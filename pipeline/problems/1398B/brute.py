"""Independent brute force: game search over multiset of 1-blocks.

Deleting a block of zeros never scores; the game reduces to players
alternately taking whole/partial 1-runs.  Brute force by memoized search
over the sorted tuple of 1-run lengths, allowing taking any amount from
any run (splitting a run leaves two runs).
"""
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def best(state):
    # state: sorted tuple of 1-run lengths; returns best score for player to move
    if not state:
        return 0
    total = sum(state)
    res = 0
    for i, r in enumerate(state):
        rest = state[:i] + state[i + 1:]
        for take in range(1, r + 1):
            for left in range(0, r - take + 1):
                right = r - take - left
                nxt = list(rest)
                if left:
                    nxt.append(left)
                if right:
                    nxt.append(right)
                nxt.sort()
                res = max(res, take + (total - take) - best(tuple(nxt)))
    return res


def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(1, int(data[0]) + 1):
        s = data[i]
        runs = tuple(sorted(len(b) for b in s.split("0") if b))
        out.append(str(best(runs)))
    print("\n".join(out))


main()
