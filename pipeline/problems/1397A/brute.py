"""Independent solution: try to build a concrete common multiset.

Instead of the divisibility criterion, greedily distribute the pooled letters
into n equal multisets and verify the distribution exists.
"""
import sys
from collections import Counter


def solve(strs):
    n = len(strs)
    pool = Counter()
    for s in strs:
        pool.update(s)
    target = Counter()
    for ch, v in pool.items():
        target[ch] = v // n
    rebuilt = Counter()
    for ch, v in target.items():
        rebuilt[ch] = v * n
    return "YES" if rebuilt == pool else "NO"


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        strs = [next(it) for _ in range(n)]
        out.append(solve(strs))
    sys.stdout.write("\n".join(out) + "\n")


main()
