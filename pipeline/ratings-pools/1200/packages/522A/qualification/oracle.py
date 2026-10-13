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
    n = r.integer(1, 200)
    depth = {'polycarp': 1}
    for _ in range(n):
        line = r.line()
        require(re.fullmatch(r'[A-Za-z0-9]{2,24} reposted [A-Za-z0-9]{2,24}', line) is not None)
        child, _, parent = line.lower().split(' ')
        require(child not in depth and parent in depth)
        depth[child] = depth[parent]+1
    return str(max(depth.values()))


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
