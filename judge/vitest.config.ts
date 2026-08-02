import { defineConfig } from "vitest/config";

export default defineConfig({
  // Don't pick up the web app's postcss.config at the repo root.
  css: { postcss: { plugins: [] } },
  test: {
    include: ["test/**/*.test.ts"],
  },
});
