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
    w, h = p.ints(2, 1, 100)
    image = [p.word(rb'[.*]+', w, w).decode('ascii') for _ in range(h)]
    lines = []
    for column in range(w):
        row = ''.join(image[r][column] * 2 for r in range(h))
        lines.extend((row, row))
    answer = '\n'.join(lines)
    p.end()
    return str(answer) + '\n'


if __name__ == '__main__':
    try:
        result = solve(sys.stdin.buffer.read())
    except (AssertionError, ValueError, IndexError):
        sys.exit(3)
    sys.stdout.write(result)
