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

def solve(data):
    rows = lines(data, 1)
    n, k = integers(rows[0], 2, 0, 1000000)
    require(1 <= n <= 100, 'n out of range')
    if k > n * n:
        return '-1'
    matrix = [[0] * n for _ in range(n)]
    for row in range(n):
        for column in range(row, n):
            cost = 1 if row == column else 2
            if k >= cost:
                matrix[row][column] = matrix[column][row] = 1
                k -= cost
    require(k == 0, 'internal remaining ones')
    return '\n'.join(' '.join(map(str, row)) for row in matrix)


if __name__ == '__main__':
    try:
        answer = solve(sys.stdin.buffer.read())
    except Invalid as error:
        print('invalid input: ' + str(error), file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(answer + '\n')
