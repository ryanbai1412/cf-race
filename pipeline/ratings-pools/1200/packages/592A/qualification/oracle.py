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
check(len(L) == 8)
for l in L:
    check(len(l) == 8 and all(ch in '.BW' for ch in l))
check('W' not in L[0] and 'B' not in L[7])


def column_configs(col):
    pawns = [(r + 1, col[r]) for r in range(8) if col[r] != '.']
    res = set()

    def rec(i, prev, wm, bm, fin):
        if i == len(pawns):
            occ = set(fin)
            wcan = bcan = False
            ok = True
            for (r0, t), f in zip(pawns, fin):
                if t == 'W':
                    if f == 1:
                        ok = False
                    elif f - 1 not in occ:
                        wcan = True
                else:
                    if f == 8:
                        ok = False
                    elif f + 1 not in occ:
                        bcan = True
            if ok:
                res.add((wm - bm, wcan, bcan))
            return
        r0, t = pawns[i]
        rng = range(max(prev + 1, 1), r0 + 1) if t == 'W' else range(max(prev + 1, r0), 9)
        for f in rng:
            rec(i + 1, f, wm + (r0 - f if t == 'W' else 0), bm + (f - r0 if t == 'B' else 0), fin + [f])

    rec(0, 0, 0, 0, [])
    return res


cols = [column_configs([L[r][c] for r in range(8)]) for c in range(8)]


def reachable_diffs(stuck_index):
    diffs = {0}
    for cfg in cols:
        opts = {d for d, wc, bc in cfg if not (wc, bc)[stuck_index]}
        diffs = {x + y for x in diffs for y in opts}
        if not diffs:
            break
    return diffs


check(0 not in reachable_diffs(0))
check(1 not in reachable_diffs(1))

INF = 100
da = db = INF
for c in range(8):
    for r in range(8):
        ch = L[r][c]
        if ch == 'W' and all(L[q][c] == '.' for q in range(r)):
            da = min(da, r)
        if ch == 'B' and all(L[q][c] == '.' for q in range(r + 1, 8)):
            db = min(db, 7 - r)
check(da < INF or db < INF)
print('A' if da <= db else 'B')
