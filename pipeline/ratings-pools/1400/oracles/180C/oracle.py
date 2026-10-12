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
    require(len(lines) == 1, "expected one string line")
    s = lines[0]
    require(1 <= len(s) <= 100000 and re.fullmatch(rb"[a-zA-Z]+", s),
            "expected 1..100000 ASCII letters")
    cost = sum(65 <= c <= 90 for c in s)
    best = cost
    for c in s:
        cost += -1 if 65 <= c <= 90 else 1
        best = min(best, cost)
    return str(best)


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
