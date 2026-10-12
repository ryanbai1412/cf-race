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


def solve(raw):
    lines = read_lines(raw, 2)
    n = integers(lines[0], 1, 1, 100)[0]
    remaining = integers(lines[1], 2 * n, 1, n)
    frequency = [0] * (n + 1)
    for value in remaining:
        frequency[value] += 1
    require(all(x == 2 for x in frequency[1:]), "each label must occur twice")
    answer = 0
    while remaining:
        partner = remaining.index(remaining[0], 1)
        answer += partner - 1
        remaining.pop(partner)
        remaining.pop(0)
    return str(answer)


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
