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
    n, m = p.ints(2, 0, 4950)
    assert 1 <= n <= 100 and m <= n * (n - 1) // 2
    graph = [set() for _ in range(n)]
    for _ in range(m):
        a, b = p.ints(2, 1, n)
        a -= 1
        b -= 1
        assert a != b and b not in graph[a]
        graph[a].add(b)
        graph[b].add(a)
    degree = list(map(len, graph))
    alive = [True] * n
    answer = 0
    while True:
        leaves = [i for i in range(n) if alive[i] and degree[i] == 1]
        if not leaves:
            break
        answer += 1
        for i in leaves:
            alive[i] = False
        for i in leaves:
            for j in graph[i]:
                if alive[j]:
                    degree[j] -= 1
    p.end()
    return str(answer) + '\n'


if __name__ == '__main__':
    try:
        result = solve(sys.stdin.buffer.read())
    except (AssertionError, ValueError, IndexError):
        sys.exit(3)
    sys.stdout.write(result)
