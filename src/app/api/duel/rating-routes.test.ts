import { beforeEach, describe, expect, it, vi } from "vitest";
import { NextRequest } from "next/server";

const fake = vi.hoisted(() => ({
  user: { id: "member" } as { id: string } | null,
  result: { ok: true } as Record<string, unknown>,
  rpc: vi.fn(),
  start: vi.fn(),
}));
vi.mock("@/lib/impersonation", () => ({ getEffectiveUser: () => fake.user }));
vi.mock("@/lib/db", () => ({ db: () => ({ rpc: fake.rpc }) }));
vi.mock("@/lib/duel", () => ({ startDuelMatch: fake.start }));
import { POST as settings } from "./settings/route";
import { POST as ready } from "./ready/route";

function request(path: string, body: Record<string, unknown>) {
  return new NextRequest(`http://localhost/api/duel/${path}`, {
    method: "POST", body: JSON.stringify({ roomId: "room", ...body }),
    headers: { "content-type": "application/json" },
  });
}

beforeEach(() => {
  fake.user = { id: "member" };
  fake.result = { ok: true };
  fake.rpc.mockReset().mockImplementation(async () => ({ data: fake.result, error: null }));
  fake.start.mockReset().mockResolvedValue({ ok: true });
});

describe("duel settings API", () => {
  it("requires a signed-in user", async () => {
    fake.user = null;
    expect((await settings(request("settings", { rating: 1200 }))).status).toBe(401);
    expect(fake.rpc).not.toHaveBeenCalled();
  });
  it.each(["800", 0, 900, 1700, null])("rejects invalid rating %s", async (rating) => {
    expect((await settings(request("settings", { rating }))).status).toBe(400);
    expect(fake.rpc).not.toHaveBeenCalled();
  });
  it("passes only validated settings and server user identity into locked RPC", async () => {
    expect((await settings(request("settings", { rating: 1600, userId: "attacker", totalTimeSec: 600 }))).status).toBe(200);
    expect(fake.rpc).toHaveBeenCalledWith("duel_lobby_action", {
      p_room_id: "room", p_user_id: "member", p_action: "settings",
      p_patch: { rating: 1600, totalTimeSec: 600 },
    });
  });
  it("preserves atomic RPC rejection, including nonmembership and locked race", async () => {
    fake.result = { ok: false, status: 409, error: "Room is not in the lobby" };
    expect((await settings(request("settings", { rating: 1000 }))).status).toBe(409);
  });
  it("rejects invalid timer values", async () => {
    for (const totalTimeSec of [-1, 0, "120", 1.5, 86401]) {
      expect((await settings(request("settings", { totalTimeSec }))).status).toBe(400);
    }
    expect(fake.rpc).not.toHaveBeenCalled();
  });
});

describe("duel ready API", () => {
  it("requires the current server settings version to ready", async () => {
    expect((await ready(request("ready", { ready: true }))).status).toBe(400);
    expect((await ready(request("ready", { ready: true, settingsVersion: -1 }))).status).toBe(400);
    expect((await ready(request("ready", { ready: true, settingsVersion: 2147483648 }))).status).toBe(400);
    expect(fake.rpc).not.toHaveBeenCalled();
  });
  it("allows unready without a version", async () => {
    const res = await ready(request("ready", { ready: false }));
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ ok: true, started: false });
  });
  it("rejects stale readiness before starting", async () => {
    fake.result = { ok: false, status: 409, error: "Settings changed" };
    expect((await ready(request("ready", { ready: true, settingsVersion: 3 }))).status).toBe(409);
    expect(fake.start).not.toHaveBeenCalled();
  });
  it("uses only the server-authoritative room snapshot and members to create a match", async () => {
    const room = { id: "room", problem_rating: 1400, settings_version: 4, status: "racing" };
    fake.result = { ok: true, claimed: true, room, playerIds: ["member", "opponent"] };
    const res = await ready(request("ready", { ready: true, settingsVersion: 4, rating: 800, playerIds: ["attacker"] }));
    expect(res.status).toBe(200);
    expect(fake.rpc).toHaveBeenCalledWith("duel_lobby_action", {
      p_room_id: "room", p_user_id: "member", p_action: "ready",
      p_patch: { ready: true, settingsVersion: 4 },
    });
    expect(fake.start).toHaveBeenCalledWith(room, ["member", "opponent"]);
  });
});
