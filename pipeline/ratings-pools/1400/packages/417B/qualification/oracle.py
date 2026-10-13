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
    n, = integers(lines[0], 1)
    require(1 <= n <= 100000, "n out of range")
    require(len(lines) == n + 1, "wrong number of submission lines")
    maximum = [-1] * 100001
    chronological = True
    for line in lines[1:]:
        x, k = integers(line, 2)
        require(0 <= x <= 100000 and 1 <= k <= 100000, "x or k out of range")
        if x > maximum[k] + 1:
            chronological = False
        maximum[k] = max(maximum[k], x)
    return "YES" if chronological else "NO"


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
