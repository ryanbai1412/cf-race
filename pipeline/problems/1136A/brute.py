"""Independent brute force: mark every read page, count unfinished chapters."""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    ch = [(int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n)]
    k = int(data[1 + 2 * n])
    read = set(range(1, k))
    cnt = 0
    for lo, hi in ch:
        if any(p not in read for p in range(lo, hi + 1)):
            cnt += 1
    print(cnt)


main()
