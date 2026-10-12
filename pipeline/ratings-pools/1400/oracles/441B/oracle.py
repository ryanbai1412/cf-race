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
    n = parse_int(t[0], 1, 3000, "n")
    v = parse_int(t[1], 1, 3000, "v")
    expect_line_count(lines, 1 + n)
    ripe = [0] * 3003
    for i in range(n):
        a, b = line_tokens(lines, 1 + i, 2)
        a = parse_int(a, 1, 3000, "a")
        b = parse_int(b, 1, 3000, "b")
        ripe[a] += b
    collected = 0
    left_prev = 0
    for d in range(1, 3002):
        cap = v
        take = min(cap, left_prev)
        collected += take
        cap -= take
        today = ripe[d]
        take = min(cap, today)
        collected += take
        left_prev = today - take
    print(collected)


main()
