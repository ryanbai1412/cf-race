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


def main():
    lines = read_lines()
    need_lines(lines, 2)
    n, k = ints(lines[0], 2, "line 1")
    rng(n, 1, 10**5, "n")
    rng(k, 0, 10**7, "k")
    a = ints(lines[1], n, "line 2")
    for v in a:
        rng(v, 0, 100, "a_i")
    rating = sum(v // 10 for v in a)
    for c in sorted(10 - v % 10 for v in a if v % 10):
        if c > k:
            k = 0
            break
        k -= c
        rating += 1
    rating += min(k // 10, 10 * n - rating)
    print(rating)


main()
