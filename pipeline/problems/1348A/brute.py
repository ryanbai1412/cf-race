import sys
from itertools import combinations


def solve(n):
    coins = [2 ** i for i in range(1, n + 1)]
    total = sum(coins)
    best = None
    for comb in combinations(range(n), n // 2):
        a = sum(coins[i] for i in comb)
        d = abs(total - 2 * a)
        if best is None or d < best:
            best = d
    return best


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = [str(solve(int(data[1 + i]))) for i in range(t)]
    print("\n".join(out))


main()
