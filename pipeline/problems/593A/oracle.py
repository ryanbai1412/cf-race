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
n, = ints(L[0], 1, 1, 100)
check(len(L) == n + 1)
words = L[1:]
check(all(re.fullmatch(r'[a-z]+', w) is not None for w in words))
check(sum(map(len, words)) <= 1000)
sets = [(set(w), len(w)) for w in words]
letters = 'abcdefghijklmnopqrstuvwxyz'
best = 0
for i in range(26):
    for j in range(i, 26):
        allowed = {letters[i], letters[j]}
        best = max(best, sum(ln for st, ln in sets if st <= allowed))
print(best)
