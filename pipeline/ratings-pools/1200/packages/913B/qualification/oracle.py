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
n, = ints(L[0], 1, 3, 1000)
check(len(L) == n)
par = [0, 0]
for i in range(1, n):
    p, = ints(L[i], 1, 1, i)
    par.append(p)
children = [[] for _ in range(n + 1)]
for v in range(2, n + 1):
    children[par[v]].append(v)
check(len(children[1]) >= 2)
ok = True
for v in range(1, n + 1):
    if children[v]:
        if sum(1 for u in children[v] if not children[u]) < 3:
            ok = False
print('Yes' if ok else 'No')
