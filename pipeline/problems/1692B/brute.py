"""Independent brute force: BFS over multiset states removing index pairs."""
import sys
from functools import lru_cache


def main():
    sys.setrecursionlimit(100000)
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []

    @lru_cache(maxsize=None)
    def best(state):
        n = len(state)
        if len(set(state)) == n:
            res = n
        else:
            res = -1
        for i in range(n):
            for j in range(i + 1, n):
                nxt = state[:i] + state[i + 1:j] + state[j + 1:]
                res = max(res, best(nxt))
        return res

    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = tuple(sorted(int(x) for x in data[pos:pos + n])); pos += n
        out.append(best(a))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
