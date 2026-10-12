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


def main():
    lines = read_lines()
    t = line_tokens(lines, 0, 2)
    n = parse_int(t[0], 2, 100, "n")
    m = parse_int(t[1], 2, 100, "m")
    expect_line_count(lines, 1 + n)
    parent = list(range(n + m))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    anyone_knows = False
    for i in range(n):
        toks = line_tokens(lines, 1 + i)
        if not toks:
            fail("empty employee line")
        k = parse_int(toks[0], 0, m, "k")
        if len(toks) != 1 + k:
            fail("employee %d: expected %d languages, got %d" % (i + 1, k, len(toks) - 1))
        seen = set()
        for tok in toks[1:]:
            a = parse_int(tok, 1, m, "a")
            if a in seen:
                fail("duplicate language in employee %d" % (i + 1))
            seen.add(a)
            anyone_knows = True
            ra, rb = find(i), find(n + a - 1)
            if ra != rb:
                parent[ra] = rb
    if not anyone_knows:
        print(n)
        return
    comps = len({find(i) for i in range(n)})
    print(comps - 1)


main()
