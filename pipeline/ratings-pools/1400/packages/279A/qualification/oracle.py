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
    require(len(lines) == 1, "expected one coordinate line")
    target_x, target_y = integers(lines[0], 2)
    require(-100 <= target_x <= 100 and -100 <= target_y <= 100,
            "coordinate out of range")
    x = y = turns = 0
    if target_x == target_y == 0:
        return "0"
    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    while True:
        dx, dy = directions[turns % 4]
        length = turns // 2 + 1
        end_x, end_y = x + dx * length, y + dy * length
        if (min(x, end_x) <= target_x <= max(x, end_x)
                and min(y, end_y) <= target_y <= max(y, end_y)):
            return str(turns)
        x, y = end_x, end_y
        turns += 1


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
