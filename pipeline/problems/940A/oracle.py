import sys
import re


class Invalid(Exception):
    pass


def require(condition):
    if not condition:
        raise Invalid


class Reader:
    def __init__(self):
        data = sys.stdin.buffer.read().replace(b'\r\n', b'\n')
        require(b'\r' not in data)
        self.lines = data.decode('ascii').split('\n')
        if self.lines[-1] == '':
            self.lines.pop()
        self.pos = 0

    def line(self):
        require(self.pos < len(self.lines))
        value = self.lines[self.pos]
        self.pos += 1
        return value

    def ints(self, count, low, high, single_spaces=False):
        line = self.line()
        pattern = r'[+-]?[0-9]+(?: [+-]?[0-9]+)*' if single_spaces else r'[ \t]*[+-]?[0-9]+(?:[ \t]+[+-]?[0-9]+)*[ \t]*'
        require(re.fullmatch(pattern, line) is not None)
        tokens = line.split()
        require(len(tokens) == count)
        values = list(map(int, tokens))
        require(all(low <= x <= high for x in values))
        return values

    def integer(self, low, high):
        return self.ints(1, low, high)[0]

    def string(self, low, high, pattern):
        value = self.line()
        require(low <= len(value) <= high and re.fullmatch(pattern, value) is not None)
        return value

    def end(self):
        require(self.pos == len(self.lines))


def solve(r):
    n, d = r.ints(2, 0, 100)
    require(n >= 1)
    a = sorted(r.ints(n, 1, 100))
    left = best = 0
    for right in range(n):
        while a[right] - a[left] > d:
            left += 1
        best = max(best, right-left+1)
    return str(n-best)


def main():
    try:
        reader = Reader()
        answer = solve(reader)
        reader.end()
    except (Invalid, ValueError, UnicodeError):
        sys.exit(3)
    sys.stdout.write(answer + '\n')


if __name__ == '__main__':
    main()
