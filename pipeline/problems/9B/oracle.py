import sys
import re


def integer(word):
    assert re.fullmatch(rb'[+-]?[0-9]+', word)
    sign = -1 if word.startswith(b'-') else 1
    digits = word.lstrip(b'+-').lstrip(b'0') or b'0'
    assert len(digits) <= 16
    return sign * int(digits)


class Reader:
    def __init__(self, data):
        data = data.replace(b'\r\n', b'\n')
        assert b'\r' not in data
        self.lines = data.split(b'\n')
        if data.endswith(b'\n'):
            self.lines.pop()
        self.index = 0

    def line(self):
        assert self.index < len(self.lines)
        value = self.lines[self.index]
        self.index += 1
        return value

    def ints(self, count, low, high):
        line = self.line()
        assert re.fullmatch(rb'[0-9+\- \t]+', line)
        words = line.split()
        assert len(words) == count
        values = [integer(w) for w in words]
        assert all(low <= x <= high for x in values)
        return values

    def word(self, pattern, low, high):
        value = self.line()
        assert low <= len(value) <= high
        assert re.fullmatch(pattern, value)
        return value

    def end(self):
        assert self.index == len(self.lines)


def solve(data):
    p = Reader(data)
    n, vb, vs = p.ints(3, 1, 1000)
    assert 2 <= n <= 100
    stops = p.ints(n, 0, 10**5)
    assert stops[0] == 0 and all(stops[i - 1] < stops[i] for i in range(1, n))
    xu, yu = p.ints(2, -10**5, 10**5)
    distances = [(x - xu)**2 + yu**2 for x in stops]
    best = 1
    for i in range(2, n):
        numerator = (stops[i] - stops[best]) * vs
        q = vb
        current, previous = distances[i], distances[best]
        residual = (previous - current) * q * q - numerator * numerator
        if residual >= 0 and residual * residual >= 4 * numerator**2 * q**2 * current:
            best = i
    answer = best + 1
    p.end()
    return str(answer) + '\n'


if __name__ == '__main__':
    try:
        result = solve(sys.stdin.buffer.read())
    except (AssertionError, ValueError, IndexError):
        sys.exit(3)
    sys.stdout.write(result)
