"""Independent brute force: exhaustive memoised search over both operations."""
import sys
from functools import lru_cache

sys.setrecursionlimit(1 << 20)


@lru_cache(maxsize=None)
def best(a, b, c):
    r = 0
    if a >= 1 and b >= 2:
        r = max(r, 3 + best(a - 1, b - 2, c))
    if b >= 1 and c >= 2:
        r = max(r, 3 + best(a, b - 1, c - 2))
    return r


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c = map(int, data[1 + 3 * i:4 + 3 * i])
        out.append(best(a, b, c))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
