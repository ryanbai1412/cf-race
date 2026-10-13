import re
import sys


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def lines(raw):
    require(isinstance(raw, bytes), 'input must be bytes')
    raw = raw.replace(b'\r\n', b'\n')
    require(b'\r' not in raw, 'bare carriage return')
    data = [line.rstrip(b' ') for line in raw.split(b'\n')]
    if data[-1] == b'':
        data.pop()
        if data and data[-1] == b'':
            data.pop()
    return data


def numbers(line, count, lower, upper):
    require(re.fullmatch(rb'[0-9]+(?: +[0-9]+)*', line) is not None,
            'expected unsigned decimal integers separated by spaces')
    tokens = line.split()
    require(len(tokens) == count, 'wrong number of integers on line')
    result = []
    for token in tokens:
        canonical = token.lstrip(b'0') or b'0'
        require(len(canonical) <= len(str(upper)), 'integer out of range')
        value = int(canonical)
        require(lower <= value <= upper, 'integer out of range')
        result.append(value)
    return result

def solve(raw):
    data = lines(raw)
    require(len(data) == 1, 'expected one input line')
    n, m = numbers(data[0], 2, 1, 10000)
    require(n != m, 'n and m must be distinct')
    steps = 0
    while m > n:
        if m % 2:
            m += 1
        else:
            m //= 2
        steps += 1
    return steps + n - m


def main():
    try:
        answer = solve(sys.stdin.buffer.read())
    except Invalid as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(answer)
    return 0


if __name__ == '__main__':
    sys.exit(main())
