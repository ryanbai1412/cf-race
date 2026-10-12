import re
import sys


class Invalid(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise Invalid(reason)


def lines_of(raw):
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        raise Invalid("input must be ASCII")
    text = text.replace("\r\n", "\n")
    require("\r" not in text, "bare carriage return")
    lines = [line.rstrip(" ") for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def integers(line, count, lo, hi, single_spaces=False):
    pattern = r"[0-9]+(?: [0-9]+)*" if single_spaces else r"[0-9]+(?: +[0-9]+)*"
    require(re.fullmatch(pattern, line) is not None, "invalid integer line")
    tokens = line.split()
    require(len(tokens) == count, "wrong integer count")
    try:
        values = [int(token) for token in tokens]
    except ValueError:
        raise Invalid("invalid integer")
    require(all(lo <= value <= hi for value in values), "integer out of range")
    return values


def main():
    try:
        result = solve(sys.stdin.buffer.read())
    except Invalid as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
    print(result)


def solve(raw):
    lines = lines_of(raw)
    require(len(lines) == 1, "wrong line count")
    m, s = integers(lines[0], 2, 0, 900)
    require(1 <= m <= 100, "m out of range")
    if s == 0:
        return "0 0" if m == 1 else "-1 -1"
    if s > 9 * m:
        return "-1 -1"
    minimum = []
    remaining = s
    for i in range(m):
        digit = max(int(i == 0), remaining - 9 * (m - i - 1))
        minimum.append(str(digit))
        remaining -= digit
    maximum = []
    remaining = s
    for _ in range(m):
        digit = min(9, remaining)
        maximum.append(str(digit))
        remaining -= digit
    return "".join(minimum) + " " + "".join(maximum)


if __name__ == "__main__":
    main()
