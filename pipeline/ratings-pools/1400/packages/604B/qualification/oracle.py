import sys
import re


def fail(msg):
    sys.stderr.write("INVALID: " + msg + "\n")
    sys.exit(1)


def read_lines():
    raw = sys.stdin.buffer.read()
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        fail("non-ascii input")
    lines = [l.rstrip(" \t\r") for l in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    for idx, l in enumerate(lines):
        if l == "":
            fail("empty line %d" % (idx + 1))
        if "\r" in l or "\t" in l:
            fail("bad whitespace on line %d" % (idx + 1))
    return lines


_INT = re.compile(r"(0|-?[1-9][0-9]*)\Z")


def toint(tok, lo, hi, name):
    if not _INT.match(tok):
        fail("bad integer token for %s: %r" % (name, tok[:30]))
    v = int(tok)
    if v < lo or v > hi:
        fail("%s=%d out of range [%d,%d]" % (name, v, lo, hi))
    return v


def need_lines(lines, cnt):
    if len(lines) != cnt:
        fail("expected %d lines, got %d" % (cnt, len(lines)))


def toks(line, cnt, where):
    t = line.split()
    if len(t) != cnt:
        fail("%s: expected %d tokens, got %d" % (where, cnt, len(t)))
    return t


def solve():
    lines = read_lines()
    need_lines(lines, 2)
    t = toks(lines[0], 2, "line 1")
    n = toint(t[0], 1, 100000, "n")
    k = toint(t[1], 1, 50000, "k")
    if not (n <= 2 * k):
        fail("n > 2k")
    s = [toint(x, 1, 1000000, "s_i") for x in toks(lines[1], n, "line 2")]
    for i in range(1, n):
        if s[i - 1] > s[i]:
            fail("not sorted")
    best = s[-1]
    p = n - k
    if p > 0:
        for i in range(p):
            v = s[i] + s[2 * p - 1 - i]
            if v > best:
                best = v
    print(best)


solve()
