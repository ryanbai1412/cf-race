import sys


def solve(n, m, rb, cb, rd, cd):
    dr, dc = 1, 1
    r, c = rb, cb
    t = 0
    while True:
        if r == rd or c == cd:
            return t
        if r + dr < 1 or r + dr > n:
            dr = -dr
        if c + dc < 1 or c + dc > m:
            dc = -dc
        r += dr
        c += dc
        t += 1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, m, rb, cb, rd, cd = (int(x) for x in data[idx : idx + 6])
        idx += 6
        out.append(str(solve(n, m, rb, cb, rd, cd)))
    print("\n".join(out))


main()
