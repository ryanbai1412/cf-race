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


def main():
    L = read_lines()
    if not L:
        fail('empty input')
    n, m, k = ints(L[0], 3, 'n m k')
    rng(n, 1, 100, 'n')
    rng(k, 1, 100, 'k')
    rng(m, 1, k, 'm')
    if len(L) != 2 + n:
        fail('expected %d lines, got %d' % (2 + n, len(L)))
    p = ints(L[1], k, 'p')
    for x in p:
        rng(x, 1, k, 'p_l')
    if len(set(p)) != k:
        fail('p not distinct')
    orders = []
    for i in range(n):
        a = ints(L[2 + i], m, 'order %d' % (i + 1))
        for x in a:
            rng(x, 1, k, 'a_ij')
        if len(set(a)) != m:
            fail('order %d not distinct' % (i + 1))
        orders.append(a)
    row = list(p)
    total = 0
    for a in orders:
        for x in a:
            idx = row.index(x)
            total += idx + 1
            del row[idx]
            row.insert(0, x)
    print(total)


main()
