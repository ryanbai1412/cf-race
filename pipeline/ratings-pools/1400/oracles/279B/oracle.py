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
    first, second = lines_of(data, 2)
    tokens = integers(first, 2, 1, 1000000000)
    n, t = tokens
    require(n <= 100000, "book count out of range")
    a = integers(second, n, 1, 10000)
    left = total = best = 0
    for right, duration in enumerate(a):
        total += duration
        while total > t:
            total -= a[left]
            left += 1
        best = max(best, right - left + 1)
    return str(best)


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
