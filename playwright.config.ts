import { defineConfig } from "@playwright/test";

/**
 * E2E suite against a local dev server + live Supabase/judge. Requires the
 * same env vars as `pnpm dev` (see .env.example); run with `pnpm test:e2e`.
 * Judged submissions are slow (real compile + full tests), hence the
 * generous timeouts and serial workers (shared DB fixtures).
 */
export default defineConfig({
  testDir: "e2e",
  timeout: 180_000,
  expect: { timeout: 15_000 },
  workers: 1,
  retries: 0,
  reporter: [["list"]],
  use: {
    baseURL: "http://localhost:3100",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "pnpm exec next dev -p 3100",
    url: "http://localhost:3100",
    reuseExistingServer: true,
    timeout: 120_000,
  },
});
