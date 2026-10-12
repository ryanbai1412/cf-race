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
from math import isqrt


def main():
    lines = read_lines()
    expect_line_count(lines, 1)
    t = line_tokens(lines, 0, 1)
    n = parse_int(t[0], 1, 10 ** 18, "n")
    best = -1
    # n <= 1e18 forces x <= 1e9, hence s(x) <= 81
    for s in range(1, 163):
        disc = s * s + 4 * n
        r = isqrt(disc)
        if r * r != disc:
            continue
        if (r - s) <= 0 or (r - s) % 2:
            continue
        x = (r - s) // 2
        if x * x + s * x != n:
            continue
        if sum(map(int, str(x))) != s:
            continue
        if best == -1 or x < best:
            best = x
    print(best)


main()
