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
    n, k = integers(lines[0], 2, 0, 100000)
    require(1 <= n <= 100000 and k <= n, "invalid n or k")
    links = integers(lines[1], n, 0, n - 1)
    require(all(parent < i for i, parent in enumerate(links, 1)), "link is not strictly earlier")
    count = [0] * (n + 1)
    for i, parent in enumerate(links, 1):
        left = max(1, i - k)
        right = min(n, i + k)
        if parent == 0:
            count[i] = right - left + 1
        else:
            parent_right = min(n, parent + k)
            count[i] = count[parent] + right - max(left - 1, parent_right)
    return " ".join(map(str, count[1:]))


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
