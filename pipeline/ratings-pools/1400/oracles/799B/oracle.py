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
    lines = read_lines(raw, 6)
    n = integers(lines[0], 1, 1, 200000)[0]
    prices = integers(lines[1], n, 1, 1000000000)
    require(len(set(prices)) == n, "prices are not distinct")
    front = integers(lines[2], n, 1, 3)
    back = integers(lines[3], n, 1, 3)
    m = integers(lines[4], 1, 1, 200000)[0]
    buyers = integers(lines[5], m, 1, 3)
    by_color: list[list[int]] = [[], [], [], []]
    for i in sorted(range(n), key=prices.__getitem__):
        by_color[front[i]].append(i)
        if back[i] != front[i]:
            by_color[back[i]].append(i)
    sold = bytearray(n)
    cursor = [0] * 4
    output = []
    for color in buyers:
        options = by_color[color]
        j = cursor[color]
        while j < len(options) and sold[options[j]]:
            j += 1
        if j == len(options):
            output.append("-1")
        else:
            i = options[j]
            sold[i] = 1
            output.append(str(prices[i]))
            j += 1
        cursor[color] = j
    return " ".join(output)


if __name__ == "__main__":
    try:
        answer = solve(sys.stdin.buffer.read())
    except ValueError as error:
        print("invalid input:", error, file=sys.stderr)
        sys.exit(1)
    print(answer)
