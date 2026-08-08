import sys


def solve(n, m):
    best = 0

    def rec(pos, left, prev, cur):
        nonlocal best
        if pos == n:
            if left == 0:
                best = max(best, cur)
            return
        for v in range(left + 1):
            add = abs(v - prev) if pos > 0 else 0
            rec(pos + 1, left - v, v, cur + add)

    rec(0, m, 0, 0)
    return best


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n, m = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        out.append(solve(n, m))
    print("\n".join(map(str, out)))


main()
