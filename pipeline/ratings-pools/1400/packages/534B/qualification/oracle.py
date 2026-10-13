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
    require(len(lines) == 2, "wrong line count")
    v1, v2 = integers(lines[0], 2, 1, 100)
    t, d = integers(lines[1], 2, 0, 100)
    require(2 <= t <= 100 and 0 <= d <= 10, "t or d out of range")
    require(abs(v1 - v2) <= (t - 1) * d, "infeasible endpoints")
    return str(sum(min(v1 + i * d, v2 + (t - 1 - i) * d) for i in range(t)))


if __name__ == "__main__":
    main()
