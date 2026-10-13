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


_PAIR = re.compile(r'[ \t]*([1-9][0-9]{0,5})[ \t]+([1-9][0-9]{0,5})\Z')
M = 200000


def main():
    lines = read_lines()
    if not lines:
        fail("empty input")
    n, k, q = ints(lines[0], 3, "line 1")
    rng(n, 1, M, "n")
    rng(q, 1, M, "q")
    rng(k, 1, n, "k")
    need_lines(lines, 1 + n + q)
    diff = [0] * (M + 2)
    match = _PAIR.match
    for i in range(1, n + 1):
        m = match(lines[i])
        if m is None:
            fail("recipe line %d malformed" % i)
        l, r = int(m.group(1)), int(m.group(2))
        if not (l <= r <= M):
            fail("recipe line %d: need 1 <= l <= r <= 200000" % i)
        diff[l] += 1
        diff[r + 1] -= 1
    pref = [0] * (M + 1)
    cur = 0
    acc = 0
    for t in range(1, M + 1):
        cur += diff[t]
        if cur >= k:
            acc += 1
        pref[t] = acc
    out = []
    for i in range(n + 1, n + q + 1):
        m = match(lines[i])
        if m is None:
            fail("query line %d malformed" % (i - n))
        a, b = int(m.group(1)), int(m.group(2))
        if not (a <= b <= M):
            fail("query line %d: need 1 <= a <= b <= 200000" % (i - n))
        out.append(pref[b] - pref[a - 1])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
