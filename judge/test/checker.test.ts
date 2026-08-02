import { describe, expect, it } from "vitest";
import { check } from "../src/checker.js";

describe("checker", () => {
  it("accepts exact match", () => {
    expect(check("1 2 3", "1 2 3").ok).toBe(true);
  });
  it("ignores trailing whitespace and newlines", () => {
    expect(check("3\n12\n0\n", "3\n12\n0   \n\n\n").ok).toBe(true);
    expect(check("hello", "hello \n").ok).toBe(true);
  });
  it("ignores differing internal whitespace (token-based)", () => {
    expect(check("1 2\n3", "1\n2 3\n").ok).toBe(true);
  });
  it("is case-insensitive for YES/NO", () => {
    expect(check("YES\nNO", "yes\nNo").ok).toBe(true);
    expect(check("Yes", "no").ok).toBe(false);
  });
  it("is case-sensitive for other tokens", () => {
    expect(check("Hello", "hello").ok).toBe(false);
  });
  it("reports token count mismatch", () => {
    const r = check("1 2 3", "1 2");
    expect(r.ok).toBe(false);
    expect(r.note).toContain("3 tokens");
  });
  it("reports first differing token", () => {
    const r = check("1 4 5", "1 5 5");
    expect(r.ok).toBe(false);
    expect(r.note).toContain("token 2");
  });
  it("compares floats with eps when enabled", () => {
    expect(check("2.3333333333", "2.33333331", 1e-6).ok).toBe(true);
    expect(check("2.3333333333", "2.34", 1e-6).ok).toBe(false);
    expect(check("1000000", "1000000.5", 1e-6).ok).toBe(true); // rel eps
    expect(check("2.5", "2.51", null).ok).toBe(false); // eps off
  });
  it("empty outputs match", () => {
    expect(check("", "\n").ok).toBe(true);
  });
});
