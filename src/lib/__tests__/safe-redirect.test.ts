import { describe, expect, it } from "vitest";
import { isSafeRedirectPath, safeRedirectPath } from "../safe-redirect";

describe("safeRedirectPath", () => {
  it.each([
    ["/ok", "/ok"],
    ["/foo?a=b#c", "/foo?a=b#c"],
  ])("preserves safe path %s", (value, expected) => {
    expect(isSafeRedirectPath(value)).toBe(true);
    expect(safeRedirectPath(value)).toBe(expected);
  });

  it.each([
    "//evil.com",
    "/\\evil.com",
    "/\t/evil.com",
    "/\n/evil.com",
    "/\r/evil.com",
    "",
  ])("falls back for unsafe path %s", (value) => {
    expect(isSafeRedirectPath(value)).toBe(false);
    expect(safeRedirectPath(value)).toBe("/");
  });

  it("falls back for missing values", () => {
    expect(safeRedirectPath(null)).toBe("/");
    expect(safeRedirectPath(undefined)).toBe("/");
  });
});
