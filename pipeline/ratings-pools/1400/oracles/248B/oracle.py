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
    n, = integers(line, 1, 1, 100000)
    if n <= 2:
        return "-1"
    offset = (-pow(10, n - 1, 210)) % 210
    if n == 3:
        return str(100 + offset)
    return "1" + "0" * (n - 4) + f"{offset:03d}"


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
