import sys
import re


def fail(msg):
    sys.stderr.write("invalid input: " + msg + "\n")
    sys.exit(1)


def read_lines():
    data = sys.stdin.buffer.read()
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError:
        fail("non-ascii bytes")
    lines = [ln.rstrip(" \t\r") for ln in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    for i, ln in enumerate(lines):
        for ch in ln:
            o = ord(ch)
            if not (32 <= o < 127 or ch == "\t"):
                fail("bad character on line %d" % (i + 1))
    return lines


_INT_RE = re.compile(r"(?:0|-?[1-9][0-9]*)\Z")


def parse_int(tok, lo, hi, name):
    if not _INT_RE.match(tok):
        fail("malformed integer for %s: %r" % (name, tok[:40]))
    v = int(tok)
    if v < lo or v > hi:
        fail("%s=%d out of range [%d, %d]" % (name, v, lo, hi))
    return v


def line_tokens(lines, idx, count=None):
    if idx >= len(lines):
        fail("missing line %d" % (idx + 1))
    t = lines[idx].split()
    if count is not None and len(t) != count:
        fail("line %d: expected %d tokens, got %d" % (idx + 1, count, len(t)))
    return t


def expect_line_count(lines, n):
    if len(lines) != n:
        fail("expected %d lines, got %d" % (n, len(lines)))

MOD = 10 ** 9 + 7


def main():
    lines = read_lines()
    expect_line_count(lines, 1)
    t = line_tokens(lines, 0, 2)
    n = parse_int(t[0], 1, 2000, "n")
    k = parse_int(t[1], 1, 2000, "k")
    # chains b1|...|bk = m: per prime power p^e of m, exponent sequences
    # 0 <= e1 <= ... <= e_{k-1} <= e_k = e, i.e. C(e + k - 1, k - 1)
    maxe = 12
    comb = [1] * (maxe + 1)
    for e in range(1, maxe + 1):
        num = 1
        den = 1
        for j in range(1, e + 1):
            num = num * (k - 1 + j)
            den = den * j
        comb[e] = (num // den) % MOD
    total = 0
    for m in range(1, n + 1):
        x = m
        prod = 1
        p = 2
        while p * p <= x:
            if x % p == 0:
                e = 0
                while x % p == 0:
                    x //= p
                    e += 1
                prod = prod * comb[e] % MOD
            p += 1
        if x > 1:
            prod = prod * comb[1] % MOD
        total += prod
    print(total % MOD)


main()
