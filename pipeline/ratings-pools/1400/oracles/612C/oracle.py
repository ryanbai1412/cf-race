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
    if not (1 <= len(s) <= 10 ** 6):
        fail('bad length %d' % len(s))
    if not set(s) <= set('<>{}[]()'):
        fail('bad character')
    kind = {'<': 0, '{': 1, '[': 2, '(': 3, '>': 4, '}': 5, ']': 6, ')': 7}
    stack = []
    push = stack.append
    pop = stack.pop
    cnt = 0
    for ch in s:
        k = kind[ch]
        if k < 4:
            push(k)
        else:
            if not stack:
                print('Impossible')
                return
            if pop() != k - 4:
                cnt += 1
    if stack:
        print('Impossible')
        return
    print(cnt)


main()
