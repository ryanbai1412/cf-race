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
    require(2 <= n <= 100 and 1 <= m <= 100, "n or m out of range")
    require(len(lines) >= m + 2, "missing edges or query count")
    parents = [list(range(n)) for _ in range(m)]
    seen = set()

    def find(parent, v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for line in lines[1:m + 1]:
        a, b, c = integers(line, 3)
        require(1 <= a < b <= n and 1 <= c <= m,
                "edge endpoints or color out of range")
        require((a, b, c) not in seen, "duplicate colored edge")
        seen.add((a, b, c))
        parent = parents[c - 1]
        parent[find(parent, a - 1)] = find(parent, b - 1)
    q, = integers(lines[m + 1], 1)
    require(1 <= q <= 100, "q out of range")
    require(len(lines) == m + q + 2, "wrong number of query lines")
    queries = []
    for line in lines[m + 2:]:
        u, v = integers(line, 2)
        require(1 <= u <= n and 1 <= v <= n and u != v, "invalid query")
        queries.append((u - 1, v - 1))
    result = []
    for u, v in queries:
        result.append(str(sum(find(parent, u) == find(parent, v)
                              for parent in parents)))
    return "\n".join(result)


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
