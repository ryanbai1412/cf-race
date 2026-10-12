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


from itertools import permutations


def answer(data):
    lines = input_lines(data)
    n, k = integers(lines[0], 2)
    require(1 <= n <= 8 and 1 <= k <= 8, "n or k out of range")
    require(len(lines) == n + 1, "wrong number of number lines")
    numbers = lines[1:]
    require(all(len(s) == k and re.fullmatch(rb"[0-9]+", s) and int(s) > 0
                for s in numbers), "expected positive k-digit string")
    digits = [[c - 48 for c in s] for s in numbers]
    best = 10 ** k
    for order in permutations(range(k)):
        low, high = 10 ** k, -1
        for row in digits:
            value = 0
            for position in order:
                value = value * 10 + row[position]
            low = min(low, value)
            high = max(high, value)
        best = min(best, high - low)
        if best == 0:
            break
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
