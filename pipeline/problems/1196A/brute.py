"""Independent brute force: enumerate which pile Alice/Bob take and the split."""
import itertools
import sys


def solve(a, b, c):
    best = 0
    for x, y, z in itertools.permutations((a, b, c)):
        for k in range(z + 1):
            best = max(best, min(x + k, y + z - k))
    return best


def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    idx = 1
    out = []
    for _ in range(q):
        a, b, c = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        idx += 3
        out.append(str(solve(a, b, c)))
    print("\n".join(out))


main()
