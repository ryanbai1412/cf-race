import sys
import re


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def lines(data, count):
    data = data.replace(b'\r\n', b'\n')
    require(b'\r' not in data, 'bare carriage return')
    rows = data.split(b'\n')
    rows = [row.rstrip(b' ') for row in rows]
    while rows and rows[-1] == b'':
        rows.pop()
    require(len(rows) == count, 'incorrect number of lines')
    return rows


def integers(row, count, low, high, single_spaces=False):
    pattern = rb'[0-9]+(?: [0-9]+)*' if single_spaces else rb'[0-9]+(?: +[0-9]+)*'
    require(re.fullmatch(pattern, row) is not None, 'invalid integer line')
    tokens = row.split(b' ')
    tokens = [token for token in tokens if token]
    require(len(tokens) == count, 'incorrect token count')
    values = []
    for token in tokens:
        normalized = token.lstrip(b'0') or b'0'
        require(len(normalized) <= len(str(high)), 'integer out of range')
        value = int(normalized)
        require(low <= value <= high, 'integer out of range')
        values.append(value)
    return values


def word(row, length, alphabet):
    require(len(row) == length, 'incorrect string length')
    require(all(c in alphabet for c in row), 'invalid string alphabet')
    return row

from collections import deque


def solve(data):
    rows = lines(data, 3)
    n, k = integers(rows[0], 2, 1, 100000)
    walls = [word(rows[1], n, b'-X'), word(rows[2], n, b'-X')]
    require(walls[0][0] == 45, 'initial left area is dangerous')
    visited = [bytearray(n), bytearray(n)]
    visited[0][0] = 1
    queue = deque([(0, 0, 0)])
    while queue:
        side, position, time = queue.popleft()
        arrival = time + 1
        for target_side, target in ((side, position + 1), (side, position - 1), (1 - side, position + k)):
            if target >= n:
                return 'YES'
            if target >= arrival and walls[target_side][target] == 45 and not visited[target_side][target]:
                visited[target_side][target] = 1
                queue.append((target_side, target, arrival))
    return 'NO'


if __name__ == '__main__':
    try:
        answer = solve(sys.stdin.buffer.read())
    except Invalid as error:
        print('invalid input: ' + str(error), file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(answer + '\n')
