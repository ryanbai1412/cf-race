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
    n = parse_int(t[0], 1, 1000, "n")
    p = parse_int(t[1], 0, n, "p")
    expect_line_count(lines, 1 + p)
    nxt = [0] * (n + 1)
    dia = [0] * (n + 1)
    has_in = [False] * (n + 1)
    for i in range(p):
        a, b, d = line_tokens(lines, 1 + i, 3)
        a = parse_int(a, 1, n, "a")
        b = parse_int(b, 1, n, "b")
        d = parse_int(d, 1, 10 ** 6, "d")
        if a == b:
            fail("self pipe")
        if nxt[a]:
            fail("house %d has two outgoing pipes" % a)
        if has_in[b]:
            fail("house %d has two incoming pipes" % b)
        nxt[a] = b
        dia[a] = d
        has_in[b] = True
    out = []
    for u in range(1, n + 1):
        if nxt[u] and not has_in[u]:
            best = dia[u]
            v = nxt[u]
            while nxt[v]:
                if dia[v] < best:
                    best = dia[v]
                v = nxt[v]
            out.append("%d %d %d" % (u, v, best))
    sys.stdout.write(str(len(out)) + "\n" + "".join(s + "\n" for s in out))


main()
