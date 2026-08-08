"""Independent brute force: repeatedly use any runnable software until stuck."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        n, k = int(data[idx]), int(data[idx + 1])
        idx += 2
        a = [int(x) for x in data[idx : idx + n]]
        idx += n
        b = [int(x) for x in data[idx : idx + n]]
        idx += n
        used = [False] * n
        changed = True
        while changed:
            changed = False
            for i in range(n):
                if not used[i] and a[i] <= k:
                    used[i] = True
                    k += b[i]
                    changed = True
        print(k)


main()
