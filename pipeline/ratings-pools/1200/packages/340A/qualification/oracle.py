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

from math import gcd

L = get_lines()
check(len(L) == 1)
x, y, a, b = ints(L[0], 4)
check(1 <= x <= 1000 and 1 <= y <= 1000 and 1 <= a <= 2 * 10**9 and 1 <= b <= 2 * 10**9 and a <= b)
l = x * y // gcd(x, y)
print(b // l - (a - 1) // l)
