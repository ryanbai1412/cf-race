import { NextRequest, NextResponse } from "next/server";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

const mocks = vi.hoisted(() => ({
  info: vi.fn(),
  list: vi.fn(),
  access: vi.fn(),
}));

vi.mock("@/lib/db", () => ({
  db: () => ({ storage: { from: () => ({ info: mocks.info, list: mocks.list }) } }),
}));
vi.mock("@/lib/session-auth", () => ({ requireSessionAccess: mocks.access }));
vi.mock("@/lib/event-auth", () => ({ requireEvent: vi.fn() }));
vi.mock("@/lib/races", () => ({ raceParticipantByStation: vi.fn() }));
vi.mock("@/lib/rate-limit", () => ({ rateLimit: () => null }));

let sequence = 0;
let sessionId: string;

function request(step: string, query: Record<string, string> = {}, body?: unknown) {
  const params = new URLSearchParams({ sessionId, step, upload: "attempt", ...query });
  return new NextRequest(`https://example.test/api/recordings?${params}`, {
    method: "POST",
    ...(body ? { headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {}),
  });
}

describe("recording metadata checks", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    sessionId = `session-${sequence++}`;
    mocks.access.mockResolvedValue({ ok: true, session: { id: sessionId, kind: "duel" } });
    mocks.info.mockResolvedValue({ data: { size: 100 }, error: null });
    mocks.list.mockResolvedValue({ data: [], error: null });
  });

  it("confirms a chunk through exact-object info without a storage search", async () => {
    const response = await POST(request("chunk-confirm", { chunk: "7", size: "100" }));
    expect(response.status).toBe(200);
    expect(mocks.info).toHaveBeenCalledOnce();
    expect(mocks.info).toHaveBeenCalledWith(`duel/${sessionId}/chunks/attempt/000007.webm`);
    expect(mocks.list).not.toHaveBeenCalled();
  });

  it("retries missing metadata without accepting a different object", async () => {
    mocks.info.mockResolvedValue({ data: null, error: { message: "not found" } });
    const response = await POST(request("chunk-confirm", { chunk: "7", size: "100" }));
    expect(response.status).toBe(409);
    expect(mocks.info).toHaveBeenCalledTimes(3);
    expect(mocks.list).not.toHaveBeenCalled();
  });

  it("rejects a size mismatch after the existing confirmation retries", async () => {
    mocks.info.mockResolvedValue({ data: { size: 101 }, error: null });
    const response = await POST(request("chunk-confirm", { chunk: "7", size: "100" }));
    expect(response.status).toBe(409);
    expect(mocks.info).toHaveBeenCalledTimes(3);
  });

  it("recognizes an already-finalized recording using its exact metadata", async () => {
    const response = await POST(request("finalize", {}, { chunks: [{ index: 0, size: 100 }] }));
    expect(response.status).toBe(200);
    expect(mocks.info).toHaveBeenCalledOnce();
    expect(mocks.info).toHaveBeenCalledWith(`duel/${sessionId}.webm`);
    expect(mocks.list).toHaveBeenCalledOnce();
    expect(mocks.list).toHaveBeenCalledWith(
      `duel/${sessionId}/chunks/attempt`, { limit: 1000, offset: 0 },
    );
  });

  it("checks session access before requesting object metadata", async () => {
    mocks.access.mockResolvedValue({ ok: false, response: NextResponse.json({}, { status: 403 }) });
    const response = await POST(request("chunk-confirm", { chunk: "7", size: "100" }));
    expect(response.status).toBe(403);
    expect(mocks.info).not.toHaveBeenCalled();
    expect(mocks.list).not.toHaveBeenCalled();
  });
});
