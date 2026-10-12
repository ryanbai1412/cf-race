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
    expect_line_count(lines, 1)
    t = line_tokens(lines, 0, 1)
    s = t[0]
    if not (1 <= len(s) <= 30) or not all("0" <= c <= "9" for c in s):
        fail("s must be 1..30 digits")
    L = len(s)
    best = -1
    for i in range(1, L - 1):
        for j in range(i + 1, L):
            total = 0
            ok = True
            for part in (s[:i], s[i:j], s[j:]):
                if len(part) > 1 and part[0] == "0":
                    ok = False
                    break
                if len(part) > 7:
                    ok = False
                    break
                v = int(part)
                if v > 10 ** 6:
                    ok = False
                    break
                total += v
            if ok and total > best:
                best = total
    print(best)


main()
