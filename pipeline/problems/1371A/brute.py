"""Independent brute force for 1371A: enumerate all set partitions of the sticks
{1..n} and take the largest number of blocks sharing the same sum. Tiny n only."""
import sys
from collections import Counter


def partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for groups in partitions(rest):
        for i in range(len(groups)):
            yield groups[:i] + [[first] + groups[i]] + groups[i + 1:]
        yield [[first]] + groups


def solve(n):
    best = 0
    for groups in partitions(list(range(1, n + 1))):
        c = Counter(sum(g) for g in groups)
        best = max(best, max(c.values()))
    return best


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = [solve(int(data[i])) for i in range(1, t + 1)]
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
