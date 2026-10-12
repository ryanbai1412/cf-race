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
    s, t = read_lines(raw, 2)
    require(1 <= len(s) <= len(t) <= 200000, "invalid string lengths")
    require(re.fullmatch(rb"[A-Za-z]+", s) is not None, "invalid message alphabet")
    require(re.fullmatch(rb"[A-Za-z]+", t) is not None, "invalid newspaper alphabet")
    need = [0] * 128
    stock = [0] * 128
    for c in s:
        need[c] += 1
    for c in t:
        stock[c] += 1
    yay = 0
    for c in range(128):
        matched = min(need[c], stock[c])
        yay += matched
        need[c] -= matched
        stock[c] -= matched
    whoops = sum(min(need[c], stock[c ^ 32]) for c in range(65, 91))
    whoops += sum(min(need[c], stock[c ^ 32]) for c in range(97, 123))
    return f"{yay} {whoops}"


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
