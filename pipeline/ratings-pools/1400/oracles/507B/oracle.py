import re
import sys


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def lines_of(data, count):
    data = data.replace(b"\r\n", b"\n")
    require(b"\r" not in data, "bare carriage return")
    lines = data.split(b"\n")
    while lines and not lines[-1].strip(b" \t"):
        lines.pop()
    require(len(lines) == count, "wrong line count")
    return lines


def integers(line, count, low, high):
    tokens = re.split(b"[ \t]+", line.strip(b" \t"))
    require(len(tokens) == count, "wrong token count")
    result = []
    for token in tokens:
        require(re.fullmatch(b"[+-]?[0-9]+", token) is not None, "invalid integer")
        digits = token[1:] if token[:1] in (b"+", b"-") else token
        digits = digits.lstrip(b"0") or b"0"
        require(len(digits) <= len(str(max(abs(low), abs(high)))), "integer out of range")
        value = int(digits) * (-1 if token[:1] == b"-" else 1)
        require(low <= value <= high, "integer out of range")
        result.append(value)
    return result


def solve(data):
    line, = lines_of(data, 1)
    values = integers(line, 5, -100000, 100000)
    r, x, y, xx, yy = values
    require(r >= 1, "radius out of range")
    from math import isqrt
    distance_squared = (x - xx) ** 2 + (y - yy) ** 2
    diameter = 2 * r
    steps = isqrt(distance_squared) // diameter
    if (steps * diameter) ** 2 < distance_squared:
        steps += 1
    return str(steps)


def main():
    try:
        answer = solve(sys.stdin.buffer.read())
    except (Invalid, ValueError) as error:
        print(str(error)[:160], file=sys.stderr)
        return 1
    print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
