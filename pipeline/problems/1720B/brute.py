"""O(n^3) brute force over all proper subsegments."""
import sys


def solve(a):
    n = len(a)
    best = 0
    for l in range(n):
        for r in range(l, n):
            if r - l + 1 == n:
                continue
            inside = a[l:r + 1]
            outside = a[:l] + a[r + 1:]
            best = max(best, max(outside) - min(outside) + max(inside) - min(inside))
    return best


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = list(map(int, data[idx:idx + n])); idx += n
        out.append(solve(a))
    print("\n".join(map(str, out)))


main()
