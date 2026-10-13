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
check(len(L) == 2)
n, s, t = ints(L[0], 3)
check(1 <= n <= 10**5 and 1 <= s <= n and 1 <= t <= n)
p = ints(L[1], n, 1, n)
check(len(set(p)) == n)
cur, steps = s, 0
ans = -1
while True:
    if cur == t:
        ans = steps
        break
    cur = p[cur - 1]
    steps += 1
    if cur == s:
        break
print(ans)
