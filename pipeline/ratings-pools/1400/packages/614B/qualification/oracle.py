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


_NUM = re.compile(r'(?:0|[1-9][0-9]*)\Z')
_BEAUT = re.compile(r'(?:0|10*)\Z')


def main():
    lines = read_lines()
    need_lines(lines, 2)
    n = ints(lines[0], 1, "line 1")[0]
    rng(n, 1, 10**5, "n")
    toks = lines[1].split()
    if len(toks) != n:
        fail("expected %d numbers, got %d" % (n, len(toks)))
    total = 0
    odd = None
    zeros = 0
    has_zero = False
    for t in toks:
        total += len(t)
        if not _NUM.match(t):
            fail("bad number token (leading zero / non-digit) %r" % t[:20])
        if _BEAUT.match(t):
            if t == "0":
                has_zero = True
            else:
                zeros += len(t) - 1
        else:
            if odd is not None:
                fail("more than one non-beautiful number")
            odd = t
    if total > 10**5:
        fail("total length %d > 100000" % total)
    if has_zero:
        sys.stdout.write("0\n")
    else:
        sys.stdout.write((odd if odd is not None else "1") + "0" * zeros + "\n")


main()
