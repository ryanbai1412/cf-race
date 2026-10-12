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

PAT = re.compile(r"([0-9])\.(0|[0-9]{0,99}[1-9])e(0|[1-9][0-9]{0,2})\Z")


def main():
    lines = read_lines()
    expect_line_count(lines, 1)
    t = line_tokens(lines, 0, 1)
    m = PAT.match(t[0])
    if not m:
        fail("not of form a.deb")
    a, d, b = m.group(1), m.group(2), int(m.group(3))
    if b > 100:
        fail("b > 100")
    if a == "0" and b != 0:
        fail("a = 0 with nonzero b")
    digits = a + d
    if len(digits) < 1 + b:
        digits += "0" * (1 + b - len(digits))
    ip = digits[:1 + b].lstrip("0") or "0"
    fp = digits[1 + b:].rstrip("0")
    print(ip + "." + fp if fp else ip)


main()
