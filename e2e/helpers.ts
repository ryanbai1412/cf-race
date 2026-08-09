import fs from "node:fs";
import path from "node:path";
import type { APIRequestContext, BrowserContext, Page } from "@playwright/test";

export const BASE = "http://localhost:3100";

/** Service-role PostgREST access for fixtures/verification (never the UI path). */
export function supa() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error("missing Supabase env for e2e");
  return { url, key };
}

export async function rest<T = unknown>(
  pathAndQuery: string,
  init?: { method?: string; body?: unknown; headers?: Record<string, string> }
): Promise<T> {
  const { url, key } = supa();
  const res = await fetch(`${url}/rest/v1/${pathAndQuery}`, {
    method: init?.method ?? "GET",
    headers: {
      apikey: key,
      authorization: `Bearer ${key}`,
      "content-type": "application/json",
      prefer: "return=representation",
      ...init?.headers,
    },
    body: init?.body === undefined ? undefined : JSON.stringify(init.body),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`REST ${pathAndQuery}: ${res.status} ${text}`);
  return (text ? JSON.parse(text) : null) as T;
}

/** The reference AC solution for a problem from the offline pipeline. */
export function refSolution(problemId: string): string {
  const p = path.join(__dirname, "..", "pipeline", "problems", problemId, "ref.py");
  return fs.readFileSync(p, "utf8");
}

export const WA_SOLUTION = "print(0)\n";

/**
 * Problems the judge can actually grade AND that have a local ref solution:
 * the judge syncs test packages from Storage (tracked in the manifest), so a
 * problem outside the manifest 404s on /submit.
 */
export function problemsWithRef(): string[] {
  const root = path.join(__dirname, "..");
  const manifest = JSON.parse(
    fs.readFileSync(path.join(root, "problems", "tests-manifest.json"), "utf8")
  ) as Record<string, unknown>;
  const dir = path.join(root, "pipeline", "problems");
  return fs
    .readdirSync(dir)
    .filter(
      (id) =>
        id in manifest && fs.existsSync(path.join(dir, id, "ref.py"))
    );
}

/**
 * Whether the judge VM has this problem's package on disk (it syncs from
 * Storage on boot only, so recently uploaded problems can be missing).
 */
export async function judgeHasProblem(problemId: string): Promise<boolean> {
  const url = process.env.JUDGE_URL;
  const token = process.env.JUDGE_TOKEN;
  if (!url || !token) throw new Error("missing judge env for e2e");
  const res = await fetch(`${url}/run`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      runId: `e2e-probe-${Date.now()}`,
      lang: "py",
      source: "pass",
      problemId,
    }),
  });
  return res.ok;
}

/** Set Monaco's active model content (typing Python via keystrokes breaks on auto-indent). */
export async function setMonaco(page: Page, code: string, lang: "cpp" | "py") {
  const language = lang === "py" ? "python" : "cpp";
  await page.waitForFunction(
    () => (window as unknown as { monaco?: unknown }).monaco !== undefined
  );
  await page.evaluate(
    ({ code, language }) => {
      const monaco = (
        window as unknown as {
          monaco: {
            editor: {
              getModels(): {
                getLanguageId(): string;
                setValue(v: string): void;
              }[];
            };
          };
        }
      ).monaco;
      const model = monaco.editor
        .getModels()
        .find((m) => m.getLanguageId() === language);
      if (!model) throw new Error(`no ${language} model`);
      model.setValue(code);
    },
    { code, language }
  );
}

/** Sign in a Supabase test user via password grant and set the auth cookie. */
export async function signInTestUser(
  context: BrowserContext,
  email: string
): Promise<{ userId: string }> {
  const { url, key } = supa();
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!anon) throw new Error("missing anon key for e2e");
  const password = process.env.E2E_TEST_USER_PASSWORD ?? "cfrace-e2e-tests";

  // Ensure the user exists with our known password (admin upsert).
  const usersRes = await fetch(`${url}/auth/v1/admin/users?page=1&per_page=1000`, {
    headers: { apikey: key, authorization: `Bearer ${key}` },
  });
  const users = (await usersRes.json()) as { users: { id: string; email: string }[] };
  let user = users.users.find((u) => u.email === email);
  if (user) {
    await fetch(`${url}/auth/v1/admin/users/${user.id}`, {
      method: "PUT",
      headers: {
        apikey: key,
        authorization: `Bearer ${key}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ password }),
    });
  } else {
    const createRes = await fetch(`${url}/auth/v1/admin/users`, {
      method: "POST",
      headers: {
        apikey: key,
        authorization: `Bearer ${key}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ email, password, email_confirm: true }),
    });
    user = (await createRes.json()) as { id: string; email: string };
  }

  const tokenRes = await fetch(`${url}/auth/v1/token?grant_type=password`, {
    method: "POST",
    headers: { apikey: anon, "content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!tokenRes.ok) throw new Error(`password grant failed for ${email}`);
  const session = await tokenRes.json();

  const ref = new URL(url).hostname.split(".")[0];
  const value = "base64-" + Buffer.from(JSON.stringify(session)).toString("base64url");
  await context.addCookies([
    {
      name: `sb-${ref}-auth-token`,
      value,
      url: BASE,
    },
  ]);
  return { userId: user!.id };
}

/** POST a JSON body to an app API route through Playwright's request context. */
export async function api<T = Record<string, unknown>>(
  request: APIRequestContext,
  route: string,
  body: unknown
): Promise<{ status: number; json: T }> {
  const res = await request.post(`${BASE}${route}`, { data: body });
  let json: T;
  try {
    json = (await res.json()) as T;
  } catch {
    json = {} as T;
  }
  return { status: res.status(), json };
}
