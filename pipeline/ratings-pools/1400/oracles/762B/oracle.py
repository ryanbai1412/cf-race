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
    if len(lines) < 2:
        fail("too few lines")
    t = toks(lines[0], 3, "line 1")
    a = toint(t[0], 0, 100000, "a")
    b = toint(t[1], 0, 100000, "b")
    c = toint(t[2], 0, 100000, "c")
    m = toint(toks(lines[1], 1, "line 2")[0], 0, 300000, "m")
    need_lines(lines, m + 2)
    usb = []
    ps2 = []
    for i in range(m):
        v, typ = toks(lines[i + 2], 2, "line %d" % (i + 3))
        val = toint(v, 1, 10 ** 9, "val")
        if typ == "USB":
            usb.append(val)
        elif typ == "PS/2":
            ps2.append(val)
        else:
            fail("bad port type on line %d" % (i + 3))
    usb.sort()
    ps2.sort()
    cnt = 0
    cost = 0
    tu = min(a, len(usb))
    tp = min(b, len(ps2))
    cnt += tu + tp
    cost += sum(usb[:tu]) + sum(ps2[:tp])
    rest = sorted(usb[tu:] + ps2[tp:])
    tc = min(c, len(rest))
    cnt += tc
    cost += sum(rest[:tc])
    print(cnt, cost)


solve()
