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
    first, second, third = lines_of(data, 3)
    n, m = integers(first, 2, 0, 100)
    a = integers(second, n + 1, -100, 100)
    b = integers(third, m + 1, -100, 100)
    require(a[0] != 0 and b[0] != 0, "zero leading coefficient")
    if n < m:
        return "0/1"
    if n > m:
        return "Infinity" if a[0] * b[0] > 0 else "-Infinity"
    from math import gcd
    divisor = gcd(a[0], b[0])
    numerator, denominator = a[0] // divisor, b[0] // divisor
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    return f"{numerator}/{denominator}"


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
