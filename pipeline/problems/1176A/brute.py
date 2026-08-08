import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def solve(n):
    if n == 1:
        return 0
    best = -1
    for p, nxt in ((2, n // 2 if n % 2 == 0 else None),
                   (3, 2 * n // 3 if n % 3 == 0 else None),
                   (5, 4 * n // 5 if n % 5 == 0 else None)):
        if nxt is None:
            continue
        r = solve(nxt)
        if r >= 0 and (best < 0 or r + 1 < best):
            best = r + 1
    return best


def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    out = [solve(int(data[i])) for i in range(1, q + 1)]
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
