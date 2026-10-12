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

from math import comb


def solve(data):
    rows = lines(data, 1)
    n, m, t = integers(rows[0], 3, 1, 60)
    require(4 <= n <= 30 and 1 <= m <= 30 and 5 <= t <= n + m, 'n, m or t out of range')
    answer = sum(comb(n, boys) * comb(m, t - boys)
                 for boys in range(4, n + 1) if 1 <= t - boys <= m)
    return str(answer)


if __name__ == '__main__':
    try:
        answer = solve(sys.stdin.buffer.read())
    except Invalid as error:
        print('invalid input: ' + str(error), file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(answer + '\n')
