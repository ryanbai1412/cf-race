import sys
import re


def bad():
    sys.exit(3)


def get_lines():
    data = sys.stdin.buffer.read()
    try:
        s = data.decode('ascii')
    except UnicodeDecodeError:
        bad()
    s = s.replace('\r\n', '\n')
    if s.endswith('\n'):
        s = s[:-1]
    if '\r' in s:
        bad()
    return s.split('\n')


_INT_LINE = re.compile(r'(?:0|-?[1-9][0-9]{0,18})(?: (?:0|-?[1-9][0-9]{0,18}))*\Z')


def ints(line, count=None, lo=None, hi=None):
    if not _INT_LINE.match(line):
        bad()
    vals = list(map(int, line.split(' ')))
    if count is not None and len(vals) != count:
        bad()
    if lo is not None and min(vals) < lo:
        bad()
    if hi is not None and max(vals) > hi:
        bad()
    return vals


def check(cond):
    if not cond:
        bad()

L = get_lines()
check(len(L) >= 2)
n, m = ints(L[0], 2, 1, 10**4)
check(len(L) == m + 2)
p = ints(L[1], n, 1, n)
check(len(set(p)) == n)
qs = []
for i in range(m):
    l, r, x = ints(L[2 + i], 3)
    check(1 <= l <= x <= r <= n)
    qs.append((l, r, x))
events = [[] for _ in range(n + 1)]
for idx, (l, r, x) in enumerate(qs):
    events[l - 1].append((idx, -1))
    events[r].append((idx, 1))
cnt = [0] * m
bit = [0] * (n + 1)
for pos in range(n + 1):
    if pos > 0:
        j = p[pos - 1]
        while j <= n:
            bit[j] += 1
            j += j & -j
    for idx, sg in events[pos]:
        v = p[qs[idx][2] - 1] - 1
        s = 0
        while v > 0:
            s += bit[v]
            v -= v & -v
        cnt[idx] += sg * s
out = ['Yes' if cnt[i] == qs[i][2] - qs[i][0] else 'No' for i in range(m)]
sys.stdout.write('\n'.join(out) + '\n')
