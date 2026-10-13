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
    t = line_tokens(lines, 0, 3)
    n = parse_int(t[0], 1, 10 ** 5, "n")
    r = parse_int(t[1], 1, 10 ** 9, "r")
    avg = parse_int(t[2], 1, min(r, 10 ** 6), "avg")
    expect_line_count(lines, 1 + n)
    exams = []
    total = 0
    for i in range(n):
        a, b = line_tokens(lines, 1 + i, 2)
        a = parse_int(a, 1, r, "a")
        b = parse_int(b, 1, 10 ** 6, "b")
        total += a
        exams.append((b, r - a))
    need = avg * n - total
    cost = 0
    if need > 0:
        exams.sort()
        for b, room in exams:
            if need <= 0:
                break
            use = room if room < need else need
            cost += use * b
            need -= use
    print(cost)


main()
