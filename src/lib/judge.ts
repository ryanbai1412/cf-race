import type {
  RunRequest,
  RunResponse,
  SubmitRequest,
  SubmitResponse,
} from "@cf-race/judge-protocol";
import type { SampleTest } from "./types";

const JUDGE_URL = process.env.JUDGE_URL;
const JUDGE_TOKEN = process.env.JUDGE_TOKEN;

export function judgeConfigured(): boolean {
  return Boolean(JUDGE_URL && JUDGE_TOKEN);
}

/**
 * Judging is side-effect free, so a request lost to a judge machine restart or
 * a transient 5xx is retried once before the attempt is reported as failed.
 */
async function judgeFetch(path: string, body: unknown): Promise<Response> {
  const send = () =>
    fetch(`${JUDGE_URL}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${JUDGE_TOKEN}`,
      },
      body: JSON.stringify(body),
      cache: "no-store",
    });
  let res: Response | null = null;
  try {
    res = await send();
    if (res.status < 500) return res;
  } catch {
    /* network error — retry below */
  }
  await new Promise((r) => setTimeout(r, 500));
  try {
    return await send();
  } catch (e) {
    if (res) return res;
    throw e;
  }
}

export async function judgeRun(args: RunRequest): Promise<RunResponse> {
  const res = await judgeFetch("/run", args);
  if (!res.ok) throw new Error(`judge /run failed: ${res.status}`);
  return (await res.json()) as RunResponse;
}

export type SubmitResult = SubmitResponse & { compileError?: string };

export async function judgeSubmit(args: SubmitRequest): Promise<SubmitResult> {
  const res = await judgeFetch("/submit", args);
  if (!res.ok) throw new Error(`judge /submit failed: ${res.status}`);
  const data = (await res.json()) as SubmitResponse;
  // The judge names the compile diagnostics `compileStderr`.
  return { ...data, compileError: data.compileStderr };
}

export function samplesToTests(
  samples: SampleTest[]
): { name: string; input: string; expected: string }[] {
  return samples.map((s, i) => ({
    name: `sample${i + 1}`,
    input: s.input,
    expected: s.output,
  }));
}
