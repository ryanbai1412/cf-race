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
    expect_line_count(lines, 8)
    pts = []
    for i in range(8):
        a, b = line_tokens(lines, i, 2)
        pts.append((parse_int(a, 0, 10 ** 6, "x"), parse_int(b, 0, 10 ** 6, "y")))
    xs = sorted({p[0] for p in pts})
    ys = sorted({p[1] for p in pts})
    ok = False
    if len(xs) == 3 and len(ys) == 3 and len(set(pts)) == 8:
        want = {(x, y) for x in xs for y in ys} - {(xs[1], ys[1])}
        ok = set(pts) == want
    print("respectable" if ok else "ugly")


main()
