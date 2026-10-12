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
check(len(L) == 4)
n, = ints(L[0], 1, 1, 10**5)
a = ints(L[1], n, 1, 1000)
S = sum(a)
check(S <= 10**6)
m, = ints(L[2], 1, 1, 10**5)
q = ints(L[3], m, 1, S)
pre = []
t = 0
for x in a:
    t += x
    pre.append(t)
sys.stdout.write('\n'.join(str(bisect_left(pre, x) + 1) for x in q) + '\n')
