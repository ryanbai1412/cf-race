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

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'B', 'H']
L = get_lines()
check(len(L) == 1)
t = L[0].split(' ')
check(len(t) == 3 and all(x in NOTES for x in t))
v = [NOTES.index(x) for x in t]
major = minor = False
for x, y, z in permutations(v):
    d1, d2 = (y - x) % 12, (z - y) % 12
    if (d1, d2) == (4, 3):
        major = True
    if (d1, d2) == (3, 4):
        minor = True
check(not (major and minor))
print('major' if major else 'minor' if minor else 'strange')
