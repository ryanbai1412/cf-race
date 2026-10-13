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
    if len(L) != 1:
        fail('expected exactly 1 line, got %d' % len(L))
    s = L[0]
    n = len(s)
    if not (1 <= n <= 100000):
        fail('bad length %d' % n)
    if not set(s) <= set('abcdefghijklmnopqrstuvwxyz'):
        fail('bad character')
    best = n + 1
    for c in set(s):
        prev = -1
        gap = 0
        i = s.find(c)
        while i != -1:
            if i - prev > gap:
                gap = i - prev
            prev = i
            i = s.find(c, i + 1)
        if n - prev > gap:
            gap = n - prev
        if gap < best:
            best = gap
    print(best)


main()
