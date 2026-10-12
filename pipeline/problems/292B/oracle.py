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
    n, m = r.ints(2, 3, 100000)
    require(n >= 4)
    parent = list(range(n))
    sizes = [1] * n
    degree = [0] * n
    edges = set()
    components = n
    def root(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for _ in range(m):
        u, v = r.ints(2, 1, n)
        u -= 1
        v -= 1
        require(u != v)
        key = min(u, v) * n + max(u, v)
        require(key not in edges)
        edges.add(key)
        degree[u] += 1
        degree[v] += 1
        u, v = root(u), root(v)
        if u != v:
            if sizes[u] < sizes[v]:
                u, v = v, u
            parent[v] = u
            sizes[u] += sizes[v]
            components -= 1
    require(components == 1)
    if degree.count(1) == 2 and degree.count(2) == n-2:
        return 'bus topology'
    if degree.count(2) == n:
        return 'ring topology'
    if degree.count(1) == n-1 and degree.count(n-1) == 1:
        return 'star topology'
    return 'unknown topology'


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
