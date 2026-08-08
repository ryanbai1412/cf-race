import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n, h, m = data[0], data[1], data[2]
    cap = [h] * (n + 1)
    for i in range(m):
        lo, hi, x = data[3 + 3 * i:6 + 3 * i]
        for p in range(lo, hi + 1):
            cap[p] = min(cap[p], x)
    print(sum(cap[p] ** 2 for p in range(1, n + 1)))


main()
