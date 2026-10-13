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
    require(len(lines) >= 2, "missing header")
    n, m = integers(lines[0], 2, 0, 2000)
    require(1 <= n <= 1000, "n out of range")
    require(len(lines) == m + 2, "wrong line count")
    values = integers(lines[1], n, 0, 100000)
    seen = set()
    answer = 0
    for line in lines[2:]:
        x, y = integers(line, 2, 1, n)
        require(x != y, "self-loop")
        edge = (min(x, y), max(x, y))
        require(edge not in seen, "duplicate undirected edge")
        seen.add(edge)
        answer += min(values[x - 1], values[y - 1])
    return str(answer)


if __name__ == "__main__":
    main()
