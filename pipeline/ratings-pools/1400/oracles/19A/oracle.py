import re
import sys

NAME = re.compile(r'[A-Za-z]{1,30}')
NUM = r'(0|[1-9][0-9]{0,2})'
MATCH = re.compile(r'([A-Za-z]{1,30})-([A-Za-z]{1,30}) ' + NUM + ':' + NUM)
INT = re.compile(r'0|[1-9][0-9]*')


def fail(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def main():
    raw = sys.stdin.buffer.read()
    try:
        text = raw.decode('ascii')
    except UnicodeDecodeError:
        fail('non-ascii input')
    lines = text.replace('\r\n', '\n').split('\n')
    lines = [ln.rstrip(' \t') for ln in lines]
    while lines and lines[-1] == '':
        lines.pop()
    for ln in lines:
        if '\r' in ln:
            fail('stray CR')
    if not lines:
        fail('empty input')
    if not INT.fullmatch(lines[0]):
        fail('bad n line')
    n = int(lines[0])
    if not 1 <= n <= 50:
        fail('n out of range')
    if n % 2:
        fail('n must be even')
    m = n * (n - 1) // 2
    if len(lines) != 1 + n + m:
        fail('expected %d lines, got %d' % (1 + n + m, len(lines)))
    names = lines[1:1 + n]
    idx = {}
    for s in names:
        if not NAME.fullmatch(s):
            fail('bad team name')
        if s in idx:
            fail('duplicate team name')
        idx[s] = len(idx)
    pts = [0] * n
    diff = [0] * n
    scored = [0] * n
    seen = set()
    for ln in lines[1 + n:]:
        mo = MATCH.fullmatch(ln)
        if not mo:
            fail('bad match line')
        a, b, x, y = mo.group(1), mo.group(2), int(mo.group(3)), int(mo.group(4))
        if a not in idx or b not in idx:
            fail('unknown team in match')
        if x > 100 or y > 100:
            fail('goals out of range')
        i, j = idx[a], idx[b]
        if i == j:
            fail('team plays itself')
        key = (min(i, j), max(i, j))
        if key in seen:
            fail('duplicate match')
        seen.add(key)
        scored[i] += x
        scored[j] += y
        diff[i] += x - y
        diff[j] += y - x
        if x > y:
            pts[i] += 3
        elif x < y:
            pts[j] += 3
        else:
            pts[i] += 1
            pts[j] += 1
    keys = [(pts[i], diff[i], scored[i]) for i in range(n)]
    if len(set(keys)) != n:
        fail('standings are ambiguous')
    order = sorted(range(n), key=lambda i: keys[i], reverse=True)
    top = sorted(names[i] for i in order[:n // 2])
    sys.stdout.write(''.join(s + '\n' for s in top))


main()
