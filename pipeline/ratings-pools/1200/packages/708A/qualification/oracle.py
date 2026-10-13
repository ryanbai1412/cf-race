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
check(len(L) == 1)
s = L[0]
check(1 <= len(s) <= 100000 and re.fullmatch(r'[a-z]+', s) is not None)
c = list(s)
n = len(c)
i = 0
while i < n and c[i] == 'a':
    i += 1
if i == n:
    c[-1] = 'z'
else:
    while i < n and c[i] != 'a':
        c[i] = chr(ord(c[i]) - 1)
        i += 1
print(''.join(c))
