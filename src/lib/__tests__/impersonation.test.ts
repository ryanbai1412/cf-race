import { describe, expect, it } from "vitest";
import {
  IMPERSONATION_TTL_MS,
  signImpersonation,
  verifyImpersonation,
} from "../impersonation";

const KEY = "test-service-role-key";
const USER = "11111111-2222-3333-4444-555555555555";

describe("impersonation cookie", () => {
  it("round-trips a freshly signed value", () => {
    const now = 1_700_000_000_000;
    const value = signImpersonation(USER, KEY, now);
    expect(verifyImpersonation(value, KEY, now + 1000)).toBe(USER);
  });

  it("rejects a tampered user id", () => {
    const now = Date.now();
    const value = signImpersonation(USER, KEY, now);
    const forged = value.replace(USER, USER.replace("1", "9"));
    expect(verifyImpersonation(forged, KEY, now)).toBeNull();
  });

  it("rejects a value signed with a different key", () => {
    const now = Date.now();
    expect(
      verifyImpersonation(signImpersonation(USER, "other", now), KEY, now)
    ).toBeNull();
  });

  it("rejects malformed values", () => {
    expect(verifyImpersonation(undefined, KEY)).toBeNull();
    expect(verifyImpersonation("", KEY)).toBeNull();
    expect(verifyImpersonation(`${USER}.abc.sig`, KEY)).toBeNull();
    expect(verifyImpersonation(`${USER}.123`, KEY)).toBeNull();
  });

  it("expires after the 1-hour TTL", () => {
    const now = Date.now();
    const value = signImpersonation(USER, KEY, now);
    expect(
      verifyImpersonation(value, KEY, now + IMPERSONATION_TTL_MS - 1000)
    ).toBe(USER);
    expect(
      verifyImpersonation(value, KEY, now + IMPERSONATION_TTL_MS + 1000)
    ).toBeNull();
  });

  it("rejects future-dated timestamps", () => {
    const now = Date.now();
    const value = signImpersonation(USER, KEY, now + 60_000);
    expect(verifyImpersonation(value, KEY, now)).toBeNull();
  });
});
