"""Independent brute force: BFS/DFS over reachable multisets (tiny n)."""
import sys
from functools import lru_cache


def solve(a):
    a = tuple(sorted(a))

    @lru_cache(maxsize=None)
    def go(state):
        if len(state) == 1:
            return True
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:
                    continue
                if abs(state[i] - state[j]) <= 1:
                    # remove the smaller of the two (index i if <=)
                    rem = i if state[i] <= state[j] else j
                    nxt = tuple(state[:rem] + state[rem + 1:])
                    if go(nxt):
                        return True
        return False

    return go(a)


def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        out.append("YES" if solve(a) else "NO")
    print("\n".join(out))


main()
