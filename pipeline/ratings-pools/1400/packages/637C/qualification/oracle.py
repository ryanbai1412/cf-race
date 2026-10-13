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
from itertools import combinations


def solve():
    lines = read_lines()
    n = toint(toks(lines[0], 1, "line 1")[0], 1, 1000, "n") if lines else fail("empty input")
    need_lines(lines, n + 1)
    codes = []
    for i in range(n):
        c = toks(lines[i + 1], 1, "code line")[0]
        if not re.fullmatch(r"[0-9]{6}", c):
            fail("code must be exactly 6 digits")
        codes.append(c)
    if len(set(codes)) != n:
        fail("codes not distinct")
    if n == 1:
        print(6)
        return
    d = 6
    for j in range(1, 6):
        hit = False
        for hidden in combinations(range(6), j):
            keep = [p for p in range(6) if p not in hidden]
            seen = set()
            for c in codes:
                key = "".join(c[p] for p in keep)
                if key in seen:
                    hit = True
                    break
                seen.add(key)
            if hit:
                break
        if hit:
            d = j
            break
    print((d - 1) // 2)


solve()
