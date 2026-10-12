import sys
import re

_INT = re.compile(r'(?:0|-?[1-9][0-9]*)\Z')


def fail(msg):
    sys.stderr.write('invalid input: %s\n' % msg)
    sys.exit(1)


def read_lines():
    data = sys.stdin.buffer.read()
    try:
        text = data.decode('ascii')
    except UnicodeDecodeError:
        fail('non-ascii bytes')
    lines = [line.rstrip(' \t\r') for line in text.split('\n')]
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def ints(line, cnt, what):
    toks = line.split(' ')
    if len(toks) != cnt:
        fail('%s: expected %d tokens, got %d' % (what, cnt, len(toks)))
    out = []
    for t in toks:
        if not _INT.match(t):
            fail('%s: bad integer token %r' % (what, t[:20]))
        out.append(int(t))
    return out


def rng(v, lo, hi, what):
    if not (lo <= v <= hi):
        fail('%s=%d out of range [%d, %d]' % (what, v, lo, hi))


HEROES = ['Anka', 'Chapay', 'Cleo', 'Troll', 'Dracul', 'Snowy', 'Hexadecimal']


def main():
    L = read_lines()
    if not L:
        fail('empty input')
    (n,) = ints(L[0], 1, 'n')
    rng(n, 0, 42, 'n')
    if len(L) != n + 2:
        fail('expected %d lines, got %d' % (n + 2, len(L)))
    idx = {h: i for i, h in enumerate(HEROES)}
    likes = set()
    for t in range(n):
        parts = L[1 + t].split(' ')
        if len(parts) != 3 or parts[1] != 'likes':
            fail('liking line %d malformed' % (t + 1))
        p, q = parts[0], parts[2]
        if p not in idx or q not in idx:
            fail('unknown hero on liking line %d' % (t + 1))
        if p == q:
            fail('hero likes himself on line %d' % (t + 1))
        if (idx[p], idx[q]) in likes:
            fail('duplicate liking on line %d' % (t + 1))
        likes.add((idx[p], idx[q]))
    exp = ints(L[n + 1], 3, 'a b c')
    for v in exp:
        rng(v, 1, 2 * 10 ** 9, 'experience')
    best = None
    for code in range(3 ** 7):
        g = []
        c = code
        for _ in range(7):
            g.append(c % 3)
            c //= 3
        sizes = [g.count(0), g.count(1), g.count(2)]
        if 0 in sizes:
            continue
        vals = [exp[t] // sizes[t] for t in range(3)]
        diff = max(vals) - min(vals)
        lk = sum(1 for (p, q) in likes if g[p] == g[q])
        key = (diff, -lk)
        if best is None or key < best:
            best = key
    print(best[0], -best[1])


main()
