import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { config } from "../src/config.js";
import { clearProblemCache } from "../src/problems.js";
import { syncProblems } from "../src/sync.js";

vi.mock("../src/config.js", () => ({ config: { problemsDir: "" } }));
vi.mock("../src/problems.js", () => ({ clearProblemCache: vi.fn() }));

const object = (name: string, version: string, size = 4) => ({
  name,
  updated_at: "2026-09-30T00:00:00Z",
  metadata: { eTag: version, size },
});

const page = (objects: ReturnType<typeof object>[], nextCursor?: string) =>
  Response.json({ objects, folders: [], hasNext: !!nextCursor, nextCursor });

describe("problem sync", () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    config.problemsDir = fs.mkdtempSync(path.join(os.tmpdir(), "judge-sync-"));
    vi.stubEnv("SUPABASE_URL", "https://example.supabase.test");
    vi.stubEnv("SUPABASE_SERVICE_ROLE_KEY", "test-service-key");
    fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
  });

  afterEach(() => {
    fs.rmSync(config.problemsDir, { recursive: true, force: true });
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.clearAllMocks();
  });

  it("lists nested objects with cursor pagination, then downloads them", async () => {
    fetchMock
      .mockResolvedValueOnce(page([object("1003A/meta.json", "v1")], "next"))
      .mockResolvedValueOnce(page([object("dev/aplusb/tests/1.in", "v2")]))
      .mockImplementation(() => Promise.resolve(new Response("test")));

    expect(await syncProblems()).toBe(2);
    const lists = fetchMock.mock.calls.filter(([url]) => url.includes("/list-v2/"));
    expect(lists).toHaveLength(2);
    expect(JSON.parse(lists[0][1].body)).toEqual({
      prefix: "", limit: 1000, with_delimiter: false,
    });
    expect(JSON.parse(lists[1][1].body).cursor).toBe("next");
    expect(lists[0][1].signal).toBeInstanceOf(AbortSignal);
    expect(fs.readFileSync(path.join(config.problemsDir, "dev/aplusb/tests/1.in"), "utf8"))
      .toBe("test");
    expect(JSON.parse(fs.readFileSync(path.join(config.problemsDir, ".sync-state.json"), "utf8")))
      .toEqual({ "1003A/meta.json": "v1", "dev/aplusb/tests/1.in": "v2" });
    expect(clearProblemCache).toHaveBeenCalledOnce();
  });

  it("keeps unchanged files and seeds state from existing matching-size files", async () => {
    fs.mkdirSync(path.join(config.problemsDir, "1003A"));
    fs.writeFileSync(path.join(config.problemsDir, "1003A/meta.json"), "test");
    fetchMock.mockImplementation(() => Promise.resolve(page([object("1003A/meta.json", "v1")])));

    expect(await syncProblems()).toBe(0);
    expect(await syncProblems()).toBe(0);
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(clearProblemCache).not.toHaveBeenCalled();
  });

  it("downloads a changed version even when its size is unchanged", async () => {
    fs.mkdirSync(path.join(config.problemsDir, "1003A"));
    fs.writeFileSync(path.join(config.problemsDir, "1003A/meta.json"), "old!");
    fs.writeFileSync(path.join(config.problemsDir, ".sync-state.json"),
      JSON.stringify({ "1003A/meta.json": "v1" }));
    fetchMock.mockResolvedValueOnce(page([object("1003A/meta.json", "v2")]))
      .mockResolvedValueOnce(new Response("new!"));

    expect(await syncProblems()).toBe(1);
    expect(fs.readFileSync(path.join(config.problemsDir, "1003A/meta.json"), "utf8"))
      .toBe("new!");
  });

  it("rejects unsafe paths before downloading or modifying local files", async () => {
    fetchMock.mockResolvedValue(page([object("../escape", "v1")]));
    await expect(syncProblems()).rejects.toThrow("unsafe object path");
    expect(fetchMock).toHaveBeenCalledOnce();
    expect(fs.readdirSync(config.problemsDir)).toEqual([]);
  });

  it("stops if a listing fails rather than committing partial state", async () => {
    fetchMock.mockResolvedValueOnce(page([object("1003A/meta.json", "v1")], "next"))
      .mockResolvedValueOnce(new Response("unavailable", { status: 503 }));
    await expect(syncProblems()).rejects.toThrow("503");
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fs.readdirSync(config.problemsDir)).toEqual([]);
  });

  it.each([undefined, "next"])("rejects a non-advancing cursor (%s)", async (cursor) => {
    fetchMock.mockResolvedValueOnce(page([], "next"))
      .mockResolvedValueOnce(Response.json({ objects: [], hasNext: true, nextCursor: cursor }));
    await expect(syncProblems()).rejects.toThrow("did not advance");
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
