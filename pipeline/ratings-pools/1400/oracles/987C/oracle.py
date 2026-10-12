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


INF = float('inf')


def main():
    L = read_lines()
    if len(L) != 3:
        fail('expected 3 lines, got %d' % len(L))
    (n,) = ints(L[0], 1, 'n')
    rng(n, 3, 3000, 'n')
    s = ints(L[1], n, 's')
    c = ints(L[2], n, 'c')
    for v in s:
        rng(v, 1, 10 ** 9, 's_i')
    for v in c:
        rng(v, 1, 10 ** 8, 'c_i')
    vals = sorted(set(s))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    U = len(vals)

    def best_less(order, key):
        tree = [INF] * (U + 1)
        res = [INF] * n
        for j in order:
            r = key(rank[s[j]]) - 1
            b = INF
            while r > 0:
                if tree[r] < b:
                    b = tree[r]
                r -= r & -r
            res[j] = b
            r = key(rank[s[j]])
            while r <= U:
                if c[j] < tree[r]:
                    tree[r] = c[j]
                r += r & -r
        return res

    left = best_less(range(n), lambda x: x)
    right = best_less(range(n - 1, -1, -1), lambda x: U + 1 - x)
    ans = INF
    for j in range(n):
        t = left[j] + c[j] + right[j]
        if t < ans:
            ans = t
    print(-1 if ans == INF else int(ans))


main()
