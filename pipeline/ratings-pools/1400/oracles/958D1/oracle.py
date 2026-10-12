from math import gcd
from collections import Counter
import re
import sys


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def read_lines(raw, count=None):
    raw = raw.replace(b"\r\n", b"\n")
    require(b"\r" not in raw, "bare CR")
    lines = [line.rstrip(b" \t") for line in raw.split(b"\n")]
    while lines and not lines[-1]:
        lines.pop()
    if count is not None:
        require(len(lines) == count, "wrong line count")
    return lines


def integers(line, count, lo, hi):
    require(re.search(rb"[^0-9+\- \t]", line) is None, "invalid integer syntax")
    tokens = line.split()
    require(len(tokens) == count, "wrong token count")
    try:
        values = list(map(int, tokens))
    except ValueError:
        raise ValueError("invalid integer syntax") from None
    require(all(lo <= x <= hi for x in values), "integer out of range")
    return values




EXPRESSION = re.compile(rb"\(([0-9]{1,2})\+([0-9]{1,2})\)/([0-9]{1,2})")


def solve(raw):
    lines = read_lines(raw)
    require(bool(lines), "missing ship count")
    m = integers(lines[0], 1, 1, 200000)[0]
    require(len(lines) == m + 1, "wrong line count")
    coordinates = []
    for line in lines[1:]:
        match = EXPRESSION.fullmatch(line)
        if match is None:
            raise ValueError("invalid expression syntax")
        a, b, c = map(int, match.groups())
        require(a > 0 and b > 0 and c > 0, "expression integer is not positive")
        numerator = a + b
        divisor = gcd(numerator, c)
        coordinates.append((numerator // divisor, c // divisor))
    frequency = Counter(coordinates)
    return " ".join(str(frequency[x]) for x in coordinates)


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
