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
check(len(L) >= 1)
n, m = ints(L[0], 2, 1, 50)
check(len(L) == n + 2)
g = [ints(L[1 + i], m, 0, 1) for i in range(n)]
a, b = ints(L[n + 1], 2, 1, 50)
check((a <= n and b <= m) or (a <= m and b <= n))
P = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(n):
    for j in range(m):
        P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] - P[i][j] + g[i][j]
best = None
for h, w in ((a, b), (b, a)):
    if h <= n and w <= m:
        for i in range(n - h + 1):
            for j in range(m - w + 1):
                s = P[i + h][j + w] - P[i][j + w] - P[i + h][j] + P[i][j]
                if best is None or s < best:
                    best = s
print(best)
