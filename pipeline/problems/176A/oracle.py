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
n, m, k = ints(L[0], 3)
check(2 <= n <= 10 and 1 <= m <= 100 and 1 <= k <= 100)
check(len(L) == 1 + n * (m + 1))
names = set()
P = []
pos = 1
for i in range(n):
    name = L[pos]
    pos += 1
    check(re.fullmatch(r'[A-Z][a-z]{0,9}', name) is not None)
    names.add(name)
    rows = []
    for j in range(m):
        a, b, c = ints(L[pos], 3)
        pos += 1
        check(1 <= b < a <= 1000 and 0 <= c <= 100)
        rows.append((a, b, c))
    P.append(rows)
check(len(names) == n)
best = 0
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        gains = sorted(((P[j][t][1] - P[i][t][0], P[i][t][2]) for t in range(m)), reverse=True)
        cap = k
        tot = 0
        for gn, c in gains:
            if gn <= 0 or cap == 0:
                break
            take = min(c, cap)
            tot += take * gn
            cap -= take
        best = max(best, tot)
print(best)
