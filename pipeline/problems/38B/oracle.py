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
    rook = p.word(rb'[a-h][1-8]', 2, 2)
    knight = p.word(rb'[a-h][1-8]', 2, 2)
    r = (rook[0] - 97, rook[1] - 49)
    k = (knight[0] - 97, knight[1] - 49)
    def jump(a, b):
        return sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2]
    assert r != k and r[0] != k[0] and r[1] != k[1] and not jump(r, k)
    answer = sum((x, y) != k and x != r[0] and y != r[1]
                 and not jump((x, y), r) and not jump((x, y), k)
                 for x in range(8) for y in range(8))
    p.end()
    return str(answer) + '\n'


if __name__ == '__main__':
    try:
        result = solve(sys.stdin.buffer.read())
    except (AssertionError, ValueError, IndexError):
        sys.exit(3)
    sys.stdout.write(result)
