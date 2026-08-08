"""Independent brute force: BFS/greedy search over states for tiny inputs.

Exhaustive search: at each step try every ordered pair (i, j) with
a_j + a_i <= k, recursing; memoize on the sorted tuple of pile sizes.
"""
import sys
from functools import lru_cache


def solve(n, k, a):
    @lru_cache(maxsize=None)
    def go(state):
        best = 0
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if state[j] + state[i] <= k:
                    nxt = list(state)
                    nxt[j] += nxt[i]
                    best = max(best, 1 + go(tuple(nxt)))
        return best

    return go(tuple(a))


def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        a = list(map(int, data[pos:pos + n])); pos += n
        out.append(str(solve(n, k, a)))
    print("\n".join(out))


main()
