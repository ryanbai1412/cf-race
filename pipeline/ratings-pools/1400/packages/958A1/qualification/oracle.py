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
    require(len(lines) >= 1, "missing header")
    n, = integers(lines[0], 1, 1, 10)
    require(len(lines) == 2 * n + 1, "wrong line count")
    require(all(len(row) == n and re.fullmatch(r"[XO]+", row) is not None
                for row in lines[1:]), "invalid map row")
    first = tuple(lines[1:n + 1])
    target = tuple(lines[n + 1:])
    for reflected in (False, True):
        grid = tuple(row[::-1] for row in first) if reflected else first
        for _ in range(4):
            if grid == target:
                return "Yes"
            grid = tuple("".join(grid[n - 1 - j][i] for j in range(n))
                         for i in range(n))
    return "No"


if __name__ == "__main__":
    main()
