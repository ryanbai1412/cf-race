import { webcrypto } from "node:crypto";
import { AuthClient } from "@supabase/supabase-js";
import { NextRequest } from "next/server";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { middleware } from "./middleware";

let project = 0;
let cookieName: string;
let accessToken: string;
let signingKey: JsonWebKey;
const user = { id: "test-user", aud: "authenticated", role: "authenticated" };

function request(expiresAt = Math.floor(Date.now() / 1000) + 3600) {
  const session = {
    access_token: accessToken,
    refresh_token: "test-refresh-token",
    token_type: "bearer",
    expires_at: expiresAt,
    user,
  };
  const cookie = `base64-${Buffer.from(JSON.stringify(session)).toString("base64url")}`;
  return new NextRequest("https://example.com/", {
    headers: { cookie: `${cookieName}=${cookie}` },
  });
}

beforeEach(async () => {
  vi.useFakeTimers();
  vi.stubGlobal("crypto", webcrypto);
  vi.stubEnv("NEXT_PUBLIC_SUPABASE_URL", `https://test-${++project}.supabase.co`);
  vi.stubEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "test-anon-key");
  cookieName = `sb-test-${project}-auth-token`;
  vi.spyOn(console, "warn").mockImplementation(() => {});
  vi.spyOn(console, "error").mockImplementation(() => {});

  const keys = await webcrypto.subtle.generateKey(
    { name: "ECDSA", namedCurve: "P-256" },
    true,
    ["sign", "verify"]
  );
  signingKey = {
    ...(await webcrypto.subtle.exportKey("jwk", keys.publicKey)),
    kid: "test-key",
    alg: "ES256",
  } as JsonWebKey;
  const header = Buffer.from(JSON.stringify({ alg: "ES256", kid: "test-key" })).toString("base64url");
  const payload = Buffer.from(JSON.stringify({
    sub: user.id,
    aud: user.aud,
    exp: Math.floor(Date.now() / 1000) + 3600,
  })).toString("base64url");
  const signature = await webcrypto.subtle.sign(
    { name: "ECDSA", hash: "SHA-256" },
    keys.privateKey,
    Buffer.from(`${header}.${payload}`)
  );
  accessToken = `${header}.${payload}.${Buffer.from(signature).toString("base64url")}`;
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
});

describe("auth middleware", () => {
  it.each(["", "theme=dark", "sb-other-auth-token=invalid", "pkce"])(
    "does not contact Supabase without a session (%s)",
    async (cookie) => {
      const fetch = vi.fn(() => new Promise<Response>(() => {}));
      vi.stubGlobal("fetch", fetch);
      const response = await middleware(new NextRequest("https://example.com/", {
        headers: { cookie: cookie === "pkce" ? `${cookieName}-code-verifier=pkce` : cookie },
      }));
      expect(response.headers.get("x-middleware-next")).toBe("1");
      expect(fetch).not.toHaveBeenCalled();
      expect(vi.getTimerCount()).toBe(0);
    }
  );

  it("verifies signed JWTs and reuses the SDK's JWKS cache across requests", async () => {
    const getClaims = vi.spyOn(AuthClient.prototype, "getClaims");
    const fetch = vi.fn(async () => Response.json({ keys: [signingKey] }));
    vi.stubGlobal("fetch", fetch);
    for (let i = 0; i < 2; i++) {
      const response = await middleware(request());
      expect(response.headers.get("x-middleware-next")).toBe("1");
    }
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/.well-known/jwks.json"),
      expect.objectContaining({ signal: expect.any(AbortSignal) })
    );
    expect(vi.getTimerCount()).toBe(0);
    for (const result of getClaims.mock.results) {
      const { data, error } = await result.value;
      expect(error).toBeNull();
      expect(data?.claims.sub).toBe(user.id);
    }
  });

  it("does not treat invalid signatures as verified claims", async () => {
    const getClaims = vi.spyOn(AuthClient.prototype, "getClaims");
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ keys: [signingKey] })));
    const parts = accessToken.split(".");
    const signature = Buffer.from(parts[2], "base64url");
    signature[0] ^= 1;
    parts[2] = signature.toString("base64url");
    accessToken = parts.join(".");
    await middleware(request());
    const { data, error } = await getClaims.mock.results[0].value;
    expect(data).toBeNull();
    expect(error?.message).toContain("Invalid JWT signature");
  });

  it("forwards refreshed session cookies and anti-cache headers", async () => {
    const fetch = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).includes("/token?")) {
        return Response.json({
          access_token: accessToken,
          refresh_token: "new-test-refresh-token",
          token_type: "bearer",
          expires_in: 3600,
          user,
        });
      }
      return Response.json({ keys: [signingKey] });
    });
    vi.stubGlobal("fetch", fetch);
    const incoming = request(Math.floor(Date.now() / 1000) - 1);
    const response = await middleware(incoming);
    expect(response.headers.get("x-middleware-next")).toBe("1");
    expect(response.cookies.get(cookieName)?.value).toContain("base64-");
    expect(incoming.cookies.get(cookieName)?.value).toBe(response.cookies.get(cookieName)?.value);
    expect(response.headers.get("cache-control")).toContain("no-store");
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it("aborts a hung JWKS request and returns a retryable, uncached 503", async () => {
    let signal: AbortSignal | undefined;
    vi.stubGlobal("fetch", vi.fn((_input, init: RequestInit) => {
      signal = init.signal as AbortSignal;
      return new Promise<Response>(() => {});
    }));
    const incoming = request();
    const originalCookie = incoming.cookies.get(cookieName)?.value;
    const pending = middleware(incoming);
    await vi.advanceTimersByTimeAsync(5000);
    const response = await pending;
    expect(signal?.aborted).toBe(true);
    expect(response.status).toBe(503);
    expect(response.headers.get("retry-after")).toBe("5");
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(response.headers.get("x-middleware-next")).toBeNull();
    expect(response.cookies.getAll()).toEqual([]);
    expect(incoming.cookies.get(cookieName)?.value).toBe(originalCookie);
  });

  it("bounds a stalled response body as well as the initial fetch", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(new ReadableStream(), {
      headers: { "Content-Type": "application/json" },
    })));
    const pending = middleware(request());
    await vi.advanceTimersByTimeAsync(5000);
    expect((await pending).status).toBe(503);
  });

  it("preserves a completed refresh if subsequent JWKS verification times out", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).includes("/token?")) {
        return Response.json({
          access_token: accessToken,
          refresh_token: "completed-test-refresh-token",
          token_type: "bearer",
          expires_in: 3600,
          user,
        });
      }
      return new Promise<Response>(() => {});
    }));
    const incoming = request(Math.floor(Date.now() / 1000) - 1);
    const originalCookie = incoming.cookies.get(cookieName)?.value;
    const pending = middleware(incoming);
    await vi.advanceTimersByTimeAsync(5000);
    const response = await pending;
    expect(response.status).toBe(503);
    expect(response.headers.get("x-middleware-next")).toBeNull();
    expect(response.cookies.get(cookieName)?.value).not.toBe(originalCookie);
    expect(response.cookies.get(cookieName)?.value).toBe(incoming.cookies.get(cookieName)?.value);
    expect(response.headers.get("cache-control")).toBe("no-store");
  });

  it("bounds refresh retries without clearing the existing session", async () => {
    const fetch = vi.fn(async () => Response.json({ message: "Unavailable" }, { status: 503 }));
    vi.stubGlobal("fetch", fetch);
    const incoming = request(Math.floor(Date.now() / 1000) - 1);
    const originalCookie = incoming.cookies.get(cookieName)?.value;
    const pending = middleware(incoming);
    await vi.advanceTimersByTimeAsync(5000);
    const response = await pending;
    expect(response.status).toBe(503);
    expect(response.cookies.getAll()).toEqual([]);
    expect(incoming.cookies.get(cookieName)?.value).toBe(originalCookie);
    const attempts = fetch.mock.calls.length;
    await vi.advanceTimersByTimeAsync(30000);
    expect(fetch).toHaveBeenCalledTimes(attempts);
    expect(incoming.cookies.get(cookieName)?.value).toBe(originalCookie);
  });

  it("ignores a refresh that completes after the auth deadline", async () => {
    let completeRefresh!: (response: Response) => void;
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>((resolve) => {
      completeRefresh = resolve;
    })));
    const incoming = request(Math.floor(Date.now() / 1000) - 1);
    const originalCookie = incoming.cookies.get(cookieName)?.value;
    const pending = middleware(incoming);
    await vi.advanceTimersByTimeAsync(5000);
    const response = await pending;
    expect(response.status).toBe(503);
    completeRefresh(Response.json({
      access_token: accessToken,
      refresh_token: "late-test-refresh-token",
      token_type: "bearer",
      expires_in: 3600,
      user,
    }));
    await vi.advanceTimersByTimeAsync(0);
    expect(incoming.cookies.get(cookieName)?.value).toBe(originalCookie);
    expect(response.cookies.getAll()).toEqual([]);
  });
});
