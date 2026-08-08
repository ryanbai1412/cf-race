"""Independent brute: check all non-empty subsequences' products."""
import math
import sys
from itertools import combinations


def solve(a):
    for k in range(1, len(a) + 1):
        for comb in combinations(a, k):
            p = 1
            for x in comb:
                p *= x
            if math.isqrt(p) ** 2 != p:
                return "YES"
    return "NO"


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx : idx + n]]
        idx += n
        out.append(solve(a))
    print("\n".join(out))


main()
