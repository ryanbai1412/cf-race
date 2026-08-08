"""Independent brute force: enumerate every height assignment (tiny inputs)."""
import itertools
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n, h, m = data[0], data[1], data[2]
    restr = [tuple(data[3 + 3 * i:6 + 3 * i]) for i in range(m)]
    best = 0
    for heights in itertools.product(range(h + 1), repeat=n):
        if all(max(heights[lo - 1:hi]) <= x for lo, hi, x in restr):
            best = max(best, sum(v * v for v in heights))
    print(best)


main()
