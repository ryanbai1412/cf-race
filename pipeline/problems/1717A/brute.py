"""O(n^2) brute force for small n."""
import sys
from math import gcd


def solve(n):
    cnt = 0
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            g = gcd(a, b)
            if a * b // g // g <= 3:
                cnt += 1
    return cnt


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    print("\n".join(str(solve(int(data[i]))) for i in range(1, t + 1)))


main()
