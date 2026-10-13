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
    require(len(lines) == 2, "expected n line and day line")
    n, = integers(lines[0], 1)
    require(1 <= n <= 100, "n out of range")
    days = integers(lines[1], n)
    require(all(0 <= value <= 3 for value in days), "day value out of range")
    rest, contest, sport = 0, n + 1, n + 1
    for day in days:
        rest, contest, sport = (min(rest, contest, sport) + 1,
                                min(rest, sport) if day & 1 else n + 1,
                                min(rest, contest) if day & 2 else n + 1)
    return str(min(rest, contest, sport))


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
