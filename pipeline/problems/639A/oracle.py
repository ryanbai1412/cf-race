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
check(len(L) >= 2)
n, k, q = ints(L[0], 3)
check(1 <= n <= 150000 and 1 <= q <= 150000 and 1 <= k <= min(6, n))
check(len(L) == q + 2)
t = ints(L[1], n, 1, 10**9)
check(len(set(t)) == n)
qs = ints(' '.join(L[2:]), 2 * q)
check(all(len(l.split(' ')) == 2 for l in L[2:]))
types = qs[0::2]
ids = qs[1::2]
check(min(types) >= 1 and max(types) <= 2 and min(ids) >= 1 and max(ids) <= n)
seen = set()
has2 = False
for ty, i in zip(types, ids):
    if ty == 1:
        check(i not in seen)
        seen.add(i)
    else:
        has2 = True
check(has2)
shown = []
out = []
for ty, i in zip(types, ids):
    if ty == 1:
        shown.append(t[i - 1])
        if len(shown) > k:
            shown.remove(min(shown))
    else:
        out.append('YES' if t[i - 1] in shown and i in seen else 'NO')
sys.stdout.write('\n'.join(out) + '\n')
