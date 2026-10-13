from collections import deque
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
    n = integers(lines[0], 1, 2, 100000)[0]
    a = integers(lines[1], n, 1, 100000)
    require(all(abs(a[i] - a[i-1]) <= 1 for i in range(1, n)), "adjacent jump exceeds one")
    low: deque[int] = deque()
    high: deque[int] = deque()
    left = answer = 0
    for right, value in enumerate(a):
        while low and a[low[-1]] >= value:
            low.pop()
        while high and a[high[-1]] <= value:
            high.pop()
        low.append(right)
        high.append(right)
        while a[high[0]] - a[low[0]] > 1:
            if low[0] == left:
                low.popleft()
            if high[0] == left:
                high.popleft()
            left += 1
        answer = max(answer, right - left + 1)
    return str(answer)


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
