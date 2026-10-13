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
    expect_line_count(lines, 2)
    t = line_tokens(lines, 0, 4)
    n = parse_int(t[0], 1, 15, "n")
    l = parse_int(t[1], 1, 10 ** 9, "l")
    r = parse_int(t[2], l, 10 ** 9, "r")
    x = parse_int(t[3], 1, 10 ** 6, "x")
    c = [parse_int(tok, 1, 10 ** 6, "c") for tok in line_tokens(lines, 1, n)]
    c.sort()
    count = 0
    full = 1 << n
    sums = [0] * full
    for mask in range(1, full):
        low = mask & -mask
        i = low.bit_length() - 1
        sums[mask] = sums[mask ^ low] + c[i]
        if mask == low:
            continue
        hi = mask.bit_length() - 1
        if l <= sums[mask] <= r and c[hi] - c[i] >= x:
            count += 1
    print(count)


main()
