"""Independent brute force: try all 2^n swap subsets (small n)."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = [int(x) for x in data[idx : idx + n]]
        idx += n
        b = [int(x) for x in data[idx : idx + n]]
        idx += n
        best = None
        for mask in range(1 << n):
            aa = [b[i] if mask >> i & 1 else a[i] for i in range(n)]
            bb = [a[i] if mask >> i & 1 else b[i] for i in range(n)]
            v = max(aa) * max(bb)
            if best is None or v < best:
                best = v
        print(best)


main()
