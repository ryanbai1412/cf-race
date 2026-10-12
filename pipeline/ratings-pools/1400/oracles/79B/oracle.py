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
from bisect import bisect_left


def solve():
    lines = read_lines()
    if not lines:
        fail("empty input")
    t0 = toks(lines[0], 4, "line 1")
    n = toint(t0[0], 1, 40000, "n")
    m = toint(t0[1], 1, 40000, "m")
    k = toint(t0[2], 1, 1000, "k")
    t = toint(t0[3], 1, 1000, "t")
    need_lines(lines, 1 + k + t)
    waste = set()
    for i in range(k):
        x, y = toks(lines[1 + i], 2, "waste line")
        a = toint(x, 1, n, "a")
        b = toint(y, 1, m, "b")
        idx = (a - 1) * m + (b - 1)
        if idx in waste:
            fail("duplicate waste cell")
        waste.add(idx)
    ws = sorted(waste)
    names = ("Carrots", "Kiwis", "Grapes")
    out = []
    for i in range(t):
        x, y = toks(lines[1 + k + i], 2, "query line")
        a = toint(x, 1, n, "i")
        b = toint(y, 1, m, "j")
        idx = (a - 1) * m + (b - 1)
        if idx in waste:
            out.append("Waste")
        else:
            out.append(names[(idx - bisect_left(ws, idx)) % 3])
    sys.stdout.write("\n".join(out) + "\n")


solve()
