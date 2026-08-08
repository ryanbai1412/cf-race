"""Independent brute force for 1353B: enumerate which a-slots get replaced by
which b-elements (at most k swaps), maximize sum(a). Small n only."""
import itertools
import sys


def solve(n, k, a, b):
    best = sum(a)
    for m in range(1, min(k, n) + 1):
        for ia in itertools.combinations(range(n), m):
            for ib in itertools.permutations(range(n), m):
                cur = list(a)
                for x, y in zip(ia, ib):
                    cur[x] = b[y]
                best = max(best, sum(cur))
    return best


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        a = list(map(int, data[pos:pos + n])); pos += n
        b = list(map(int, data[pos:pos + n])); pos += n
        out.append(solve(n, k, a, b))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
