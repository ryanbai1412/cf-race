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
    t, sx, sy, ex, ey = p.ints(5, -10**9, 10**9)
    assert 1 <= t <= 10**5 and (sx, sy) != (ex, ey)
    winds = p.word(rb'[ESWN]+', t, t)
    dx, dy = ex - sx, ey - sy
    answer = -1
    for second, wind in enumerate(winds, 1):
        if wind == 69 and dx > 0:
            dx -= 1
        elif wind == 87 and dx < 0:
            dx += 1
        elif wind == 78 and dy > 0:
            dy -= 1
        elif wind == 83 and dy < 0:
            dy += 1
        if dx == dy == 0:
            answer = second
            break
    p.end()
    return str(answer) + '\n'


if __name__ == '__main__':
    try:
        result = solve(sys.stdin.buffer.read())
    except (AssertionError, ValueError, IndexError):
        sys.exit(3)
    sys.stdout.write(result)
