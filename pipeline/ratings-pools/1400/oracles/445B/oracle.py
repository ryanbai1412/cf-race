import re
import sys


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def input_lines(data):
    data = data.replace(b"\r\n", b"\n")
    require(b"\r" not in data, "bare CR in input")
    lines = [line.rstrip(b" ") for line in data.split(b"\n")]
    while lines and not lines[-1]:
        lines.pop()
    require(bool(lines) and all(lines), "empty input or interior blank line")
    return lines


def integers(line, count):
    require(not line.startswith(b" "), "leading space")
    tokens = [token for token in line.split(b" ") if token]
    require(len(tokens) == count, "wrong integer count on line")
    require(all(re.fullmatch(rb"[+-]?[0-9]+", token) for token in tokens),
            "invalid decimal integer")
    return [int(token) for token in tokens]


def answer(data):
    lines = input_lines(data)
    n, m = integers(lines[0], 2)
    require(1 <= n <= 50 and 0 <= m <= n * (n - 1) // 2,
            "n or m out of range")
    require(len(lines) == m + 1, "wrong number of edge lines")
    parent = list(range(n))
    seen = set()
    components = n

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for line in lines[1:]:
        x, y = integers(line, 2)
        require(1 <= x < y <= n, "edge endpoints out of range or unordered")
        require((x, y) not in seen, "duplicate edge")
        seen.add((x, y))
        left, right = find(x - 1), find(y - 1)
        if left != right:
            parent[left] = right
            components -= 1
    return str(1 << (n - components))


def main():
    data = sys.stdin.buffer.read()
    try:
        output = answer(data)
    except ValueError as error:
        print("invalid input: " + str(error), file=sys.stderr)
        return 1
    sys.stdout.write(output + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
