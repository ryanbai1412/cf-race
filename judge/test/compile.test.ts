import { afterEach, expect, it, vi } from "vitest";

vi.mock("../src/sandbox.js", () => ({ sandboxRun: vi.fn() }));

afterEach(() => {
  vi.unstubAllEnvs();
  vi.resetAllMocks();
  vi.resetModules();
});

it.each(["debug", "submit"] as const)(
  "enforces the configured compiler memory limit in %s mode",
  async (mode) => {
    vi.stubEnv("JUDGE_TOKEN", "test");
    vi.stubEnv("COMPILE_MEMORY_MB", "1536");
    const { sandboxRun } = await import("../src/sandbox.js");
    vi.mocked(sandboxRun).mockRejectedValue(new Error("stop before cache writes"));
    const { compile } = await import("../src/compile.js");

    await expect(compile("cpp", mode, "int main(){return 1536;}"))
      .rejects.toThrow("stop before cache writes");
    expect(sandboxRun).toHaveBeenCalledWith(
      expect.objectContaining({
        memoryLimitMb: 1536,
        timeLimitMs: 20000,
        wallTimeMs: 30000,
        procs: 16,
      }),
      { collect: ["prog"] }
    );
  }
);
