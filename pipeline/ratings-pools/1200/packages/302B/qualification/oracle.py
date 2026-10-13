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

from bisect import bisect_left

L = get_lines()
check(len(L) >= 1)
n, m = ints(L[0], 2, 1, 10**5)
check(len(L) == n + 2)
pre = []
tot = 0
for i in range(n):
    c, t = ints(L[1 + i], 2, 1, 10**9)
    tot += c * t
    check(tot <= 10**9)
    pre.append(tot)
v = ints(L[n + 1], m, 1, tot)
for i in range(m - 1):
    check(v[i] < v[i + 1])
sys.stdout.write('\n'.join(str(bisect_left(pre, x) + 1) for x in v) + '\n')
