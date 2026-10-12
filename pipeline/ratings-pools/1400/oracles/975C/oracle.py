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
from bisect import bisect_right


def solve():
    lines = read_lines()
    need_lines(lines, 3)
    t = toks(lines[0], 2, "line 1")
    n = toint(t[0], 1, 200000, "n")
    q = toint(t[1], 1, 200000, "q")
    a = [toint(v, 1, 10 ** 9, "a_i") for v in toks(lines[1], n, "line 2")]
    ks = [toint(v, 1, 10 ** 14, "k_i") for v in toks(lines[2], q, "line 3")]
    pre = []
    s = 0
    for v in a:
        s += v
        pre.append(s)
    total = s
    cur = 0
    out = []
    for k in ks:
        cur += k
        if cur >= total:
            cur = 0
            out.append(n)
        else:
            out.append(n - bisect_right(pre, cur))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


solve()
