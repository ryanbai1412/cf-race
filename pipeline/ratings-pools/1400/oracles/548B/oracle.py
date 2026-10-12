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


def score(row):
    return max(map(len, ''.join(row).split('0')))


def main():
    L = read_lines()
    if not L:
        fail('empty input')
    n, m, q = ints(L[0], 3, 'n m q')
    rng(n, 1, 500, 'n')
    rng(m, 1, 500, 'm')
    rng(q, 1, 5000, 'q')
    if len(L) != 1 + n + q:
        fail('expected %d lines, got %d' % (1 + n + q, len(L)))
    rows = []
    for i in range(n):
        t = L[1 + i].split(' ')
        if len(t) != m:
            fail('grid row %d: expected %d tokens, got %d' % (i + 1, m, len(t)))
        for x in t:
            if x != '0' and x != '1':
                fail('grid row %d: bad cell %r' % (i + 1, x[:20]))
        rows.append(t)
    best = [score(r) for r in rows]
    out = []
    for k in range(q):
        i, j = ints(L[1 + n + k], 2, 'query %d' % (k + 1))
        rng(i, 1, n, 'i')
        rng(j, 1, m, 'j')
        r = rows[i - 1]
        r[j - 1] = '1' if r[j - 1] == '0' else '0'
        best[i - 1] = score(r)
        out.append(max(best))
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
