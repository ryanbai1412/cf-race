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
    rows = lines(data, 2)
    n, k, x = integers(rows[0], 3, 1, 100)
    require(x <= k, 'x exceeds k')
    colors = integers(rows[1], n, 1, k)
    runs = []
    for color in colors:
        if runs and runs[-1][0] == color:
            runs[-1][1] += 1
            require(runs[-1][1] <= 2, 'initial triple')
        else:
            runs.append([color, 1])
    answer = 0
    for center, (color, size) in enumerate(runs):
        if color != x or size != 2:
            continue
        removed = size
        left, right = center - 1, center + 1
        while left >= 0 and right < len(runs):
            if runs[left][0] != runs[right][0] or runs[left][1] + runs[right][1] < 3:
                break
            removed += runs[left][1] + runs[right][1]
            left -= 1
            right += 1
        answer = max(answer, removed)
    return str(answer)


if __name__ == '__main__':
    try:
        answer = solve(sys.stdin.buffer.read())
    except Invalid as error:
        print('invalid input: ' + str(error), file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(answer + '\n')
