import math
import sys
from itertools import combinations


def possible(n, m):
    # vertices of n-gon at angles 2*pi*k/n; an inscribed regular m-gon with
    # the same center uses m vertices equally spaced in angle.
    pts = [k / n for k in range(n)]  # fractions of full turn
    for comb in combinations(range(n), m):
        angs = sorted(pts[k] for k in comb)
        gaps = [angs[(i + 1) % m] - angs[i] for i in range(m - 1)]
        gaps.append(1 - angs[-1] + angs[0])
        if all(abs(g - 1.0 / m) < 1e-9 for g in gaps):
            return True
    return False


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n, m = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        out.append("YES" if possible(n, m) else "NO")
    print("\n".join(out))


main()
