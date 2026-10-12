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
    need_lines(lines, 3)
    s = toks(lines[0], 1, "line 1")[0]
    n = len(s)
    if not (2 <= n <= 200000):
        fail("|s| out of range")
    if not re.fullmatch(r"[a-z]+", s):
        fail("s must be lowercase latin")
    m = toint(toks(lines[1], 1, "line 2")[0], 1, 100000, "m")
    at = toks(lines[2], m, "line 3")
    cnt = [0] * (n // 2 + 2)
    for tk in at:
        a = toint(tk, 1, n // 2, "a_i")
        cnt[a] += 1
    res = list(s)
    par = 0
    for i in range(1, n // 2 + 1):
        par ^= cnt[i] & 1
        if par:
            res[i - 1], res[n - i] = res[n - i], res[i - 1]
    sys.stdout.write("".join(res) + "\n")


solve()
