"""Independent brute force: exact subset-sum DP over 1..n (small n only)."""
import sys


def main():
    n = int(sys.stdin.read().split()[0])
    total = n * (n + 1) // 2
    reach = 1  # bitset of reachable subset sums
    for v in range(1, n + 1):
        reach |= reach << v
    best = total
    for s in range(total + 1):
        if reach >> s & 1:
            best = min(best, abs(total - 2 * s))
    print(best)


main()
