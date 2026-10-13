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

from itertools import permutations

L = get_lines()
check(len(L) == 3)
pairs = set()
less = []
for l in L:
    check(len(l) == 3 and l[0] in 'ABC' and l[2] in 'ABC' and l[1] in '<>' and l[0] != l[2])
    pairs.add(frozenset((l[0], l[2])))
    less.append((l[0], l[2]) if l[1] == '<' else (l[2], l[0]))
check(len(pairs) == 3)
ans = 'Impossible'
for p in permutations('ABC'):
    pos = {c: i for i, c in enumerate(p)}
    if all(pos[x] < pos[y] for x, y in less):
        ans = ''.join(p)
print(ans)
