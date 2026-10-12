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
    if len(L) != 2:
        fail('expected 2 lines, got %d' % len(L))
    (n,) = ints(L[0], 1, 'n')
    rng(n, 1, 100000, 'n')
    s = L[1]
    if len(s) != n:
        fail('string length %d != n=%d' % (len(s), n))
    if not set(s) <= {'b', 'r'}:
        fail('bad character')
    even, odd = s[0::2], s[1::2]
    start_r = max(even.count('b'), odd.count('r'))
    start_b = max(even.count('r'), odd.count('b'))
    print(min(start_r, start_b))


main()
