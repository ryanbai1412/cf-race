export interface CheckResult {
  ok: boolean;
  note?: string;
}

const YESNO = new Set(["yes", "no"]);

function isNumeric(tok: string): boolean {
  if (tok.length === 0) return false;
  const n = Number(tok);
  return !Number.isNaN(n) && /^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(tok);
}

/**
 * CF-style token comparison. Splits both outputs on whitespace (so trailing
 * whitespace/newlines are ignored), compares token by token. YES/NO tokens are
 * case-insensitive. If floatEps is set, numeric tokens compare with abs/rel eps.
 */
export function check(
  expected: string,
  actual: string,
  floatEps?: number | null
): CheckResult {
  const exp = expected.split(/\s+/).filter((t) => t.length > 0);
  const act = actual.split(/\s+/).filter((t) => t.length > 0);
  if (exp.length !== act.length) {
    return {
      ok: false,
      note: `expected ${exp.length} tokens, got ${act.length}`,
    };
  }
  for (let i = 0; i < exp.length; i++) {
    const e = exp[i];
    const a = act[i];
    if (e === a) continue;
    const el = e.toLowerCase();
    const al = a.toLowerCase();
    if (YESNO.has(el) && el === al) continue;
    if (floatEps != null && isNumeric(e) && isNumeric(a)) {
      const en = Number(e);
      const an = Number(a);
      const diff = Math.abs(en - an);
      if (diff <= floatEps || diff <= floatEps * Math.abs(en)) continue;
      return {
        ok: false,
        note: `token ${i + 1} differs: expected ${e}, got ${a} (eps ${floatEps})`,
      };
    }
    return { ok: false, note: `token ${i + 1} differs: expected ${e}, got ${a}` };
  }
  return { ok: true };
}
