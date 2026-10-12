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
    lines = read_lines(raw, 3)
    n = integers(lines[0], 1, 1, 500000)[0]
    p = integers(lines[1], n, 1, 1000000000)
    teams = lines[2]
    require(len(teams) == n and re.fullmatch(rb"[AB]+", teams) is not None, "invalid teams")
    initial = gain = largest = smallest = 0
    for value, team in zip(p, teams):
        if team == 66:
            initial += value
            gain -= value
        else:
            gain += value
        largest = max(largest, gain)
        smallest = min(smallest, gain)
    return str(initial + max(largest, gain - smallest))


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
