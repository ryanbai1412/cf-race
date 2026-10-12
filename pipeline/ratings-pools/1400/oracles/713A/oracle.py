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
    if not lines:
        fail("empty input")
    t = toint(toks(lines[0], 1, "line 1")[0], 1, 100000, "t")
    need_lines(lines, t + 1)
    num_re = re.compile(r"(0|[1-9][0-9]{0,17})\Z")
    pat_re = re.compile(r"[01]{1,18}\Z")
    tr = str.maketrans("0123456789", "0101010101")
    mult = {}
    cnt = {}
    out = []
    has_q = False
    for i in range(1, t + 1):
        tk = toks(lines[i], 2, "line %d" % (i + 1))
        c, x = tk
        if c == "+" or c == "-":
            if not num_re.match(x):
                fail("bad a_i on line %d" % (i + 1))
            key = int(x.translate(tr), 2)
            if c == "+":
                mult[x] = mult.get(x, 0) + 1
                cnt[key] = cnt.get(key, 0) + 1
            else:
                if mult.get(x, 0) == 0:
                    fail("removing absent integer on line %d" % (i + 1))
                mult[x] -= 1
                cnt[key] -= 1
        elif c == "?":
            if not pat_re.match(x):
                fail("bad pattern on line %d" % (i + 1))
            has_q = True
            out.append(cnt.get(int(x, 2), 0))
        else:
            fail("bad op on line %d" % (i + 1))
    if not has_q:
        fail("no '?' query")
    sys.stdout.write("\n".join(map(str, out)) + "\n")


solve()
