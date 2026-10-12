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
    require(len(lines) >= 3, "missing header")
    k, = integers(lines[0], 1, 1, 2000)
    s = lines[1]
    require(re.fullmatch(r"[a-z]{1,100}", s) is not None, "invalid initial string")
    n, = integers(lines[2], 1, 0, 20000)
    require(len(lines) == n + 3, "wrong line count")
    operations = []
    for line in lines[3:3 + int(lines[2])]:
        match = re.fullmatch(r"([0-9]+) +([a-z])", line)
        require(match is not None, "invalid operation line")
        try:
            p = int(match[1])
        except ValueError:
            raise Invalid("invalid occurrence number")
        require(1 <= p <= 200000, "occurrence number out of range")
        operations.append((p, ord(match[2]) - 97))
    t = s * k
    require(n < len(t), "final name must be nonempty")
    positions = [[] for _ in range(26)]
    for i, c in enumerate(t):
        positions[ord(c) - 97].append(i)
    trees = [[0] + [i & -i for i in range(1, len(pos) + 1)] for pos in positions]
    counts = [len(pos) for pos in positions]
    alive = bytearray([1]) * len(t)
    for p, c in operations:
        require(p <= counts[c], "deleted occurrence does not exist")
        tree = trees[c]
        size = len(tree) - 1
        index = 0
        step = 1 << (size.bit_length() - 1)
        while step:
            candidate = index + step
            if candidate <= size and tree[candidate] < p:
                p -= tree[candidate]
                index = candidate
            step >>= 1
        alive[positions[c][index]] = 0
        index += 1
        while index <= size:
            tree[index] -= 1
            index += index & -index
        counts[c] -= 1
    return "".join(c for i, c in enumerate(t) if alive[i])


if __name__ == "__main__":
    main()
