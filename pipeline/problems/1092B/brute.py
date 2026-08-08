"""Independent brute force: minimum-cost perfect pairing by recursion."""
import sys
from functools import lru_cache


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = sorted(map(int, data[1:1 + n]))

    @lru_cache(maxsize=None)
    def best(mask):
        if mask == (1 << n) - 1:
            return 0
        i = 0
        while mask >> i & 1:
            i += 1
        res = float("inf")
        for j in range(i + 1, n):
            if not (mask >> j & 1):
                res = min(res, abs(a[j] - a[i]) + best(mask | 1 << i | 1 << j))
        return res

    print(best(0))


main()
