import sys


def solve(n, m, a):
    s = sum(a)
    best = 0
    for a1 in range(m + 1):
        rest = s - a1
        if 0 <= rest <= (n - 1) * m:
            best = max(best, a1)
    return best


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, m = int(data[idx]), int(data[idx + 1]); idx += 2
        a = [int(data[idx + i]) for i in range(n)]; idx += n
        out.append(solve(n, m, a))
    print("\n".join(map(str, out)))


main()
