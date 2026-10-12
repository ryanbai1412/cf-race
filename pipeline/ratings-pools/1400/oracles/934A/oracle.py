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
    if len(L) != 3:
        fail('expected 3 lines, got %d' % len(L))
    n, m = ints(L[0], 2, 'n m')
    rng(n, 2, 50, 'n')
    rng(m, 2, 50, 'm')
    a = ints(L[1], n, 'a')
    b = ints(L[2], m, 'b')
    for v in a + b:
        rng(v, -10 ** 9, 10 ** 9, 'brightness')
    bmax, bmin = max(b), min(b)
    best = [max(x * bmax, x * bmin) for x in a]
    ans = min(max(best[:i] + best[i + 1:]) for i in range(n))
    print(ans)


main()
