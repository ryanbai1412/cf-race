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
n, t = ints(L[0], 2, 1, 1000)
check(len(L) == n + 1)
iv = []
for i in range(n):
    x, a = ints(L[1 + i], 2)
    check(-1000 <= x <= 1000 and 1 <= a <= 1000)
    iv.append((2 * x - a, 2 * x + a))
iv.sort()
for i in range(n - 1):
    check(iv[i][1] <= iv[i + 1][0])
ans = 2
for i in range(n - 1):
    g = iv[i + 1][0] - iv[i][1]
    if g > 2 * t:
        ans += 2
    elif g == 2 * t:
        ans += 1
print(ans)
