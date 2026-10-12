import sys
import re


def fail(msg):
    sys.stderr.write("INVALID: " + msg + "\n")
    sys.exit(1)


_BAD_BYTE = re.compile(rb'[^\x20-\x7e\t\r\n]')
_INT = re.compile(r'(?:0|-?[1-9][0-9]*)\Z')


def read_lines():
    data = sys.stdin.buffer.read()
    if _BAD_BYTE.search(data):
        fail("non-printable or non-ASCII byte in input")
    out = []
    for l in data.decode('ascii').split('\n'):
        if l.endswith('\r'):
            l = l[:-1]
        if '\r' in l:
            fail("stray CR inside a line")
        out.append(l.rstrip(' \t'))
    while out and out[-1] == '':
        out.pop()
    return out


def ints(line, cnt, what):
    toks = line.split()
    if len(toks) != cnt:
        fail("%s: expected %d tokens, got %d" % (what, cnt, len(toks)))
    res = []
    for t in toks:
        if len(t) > 12 or not _INT.match(t):
            fail("%s: bad integer token %r" % (what, t[:20]))
        res.append(int(t))
    return res


def rng(v, lo, hi, what):
    if not (lo <= v <= hi):
        fail("%s=%d out of [%d, %d]" % (what, v, lo, hi))


def need_lines(lines, cnt):
    if len(lines) != cnt:
        fail("expected %d non-trailing lines, got %d" % (cnt, len(lines)))


from math import gcd


def main():
    lines = read_lines()
    if not lines:
        fail("empty input")
    n, x0, y0 = ints(lines[0], 3, "line 1")
    rng(n, 1, 1000, "n")
    rng(x0, -10**4, 10**4, "x0")
    rng(y0, -10**4, 10**4, "y0")
    need_lines(lines, n + 1)
    dirs = set()
    for i in range(n):
        x, y = ints(lines[1 + i], 2, "trooper %d" % (i + 1))
        rng(x, -10**4, 10**4, "x")
        rng(y, -10**4, 10**4, "y")
        dx, dy = x - x0, y - y0
        if dx == 0 and dy == 0:
            fail("trooper %d stands on the gun" % (i + 1))
        g = gcd(abs(dx), abs(dy))
        dx //= g
        dy //= g
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        dirs.add((dx, dy))
    print(len(dirs))


main()
