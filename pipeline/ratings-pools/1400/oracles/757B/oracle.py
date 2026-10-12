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
    n = integers(lines[0], 1, 1, 100000)[0]
    strengths = integers(lines[1], n, 1, 100000)
    upper = max(strengths)
    frequency = [0] * (upper + 1)
    for value in strengths:
        frequency[value] += 1
    composite = bytearray(upper + 1)
    answer = 1
    for p in range(2, upper + 1):
        if not composite[p]:
            answer = max(answer, sum(frequency[p::p]))
            if p * p <= upper:
                start = p * p
                composite[start::p] = b"\x01" * ((upper - start) // p + 1)
    return str(answer)


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
