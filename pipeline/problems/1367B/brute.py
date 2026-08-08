"""Independent brute force for 1367B: over all permutations of the array, keep
the ones producing a good array and take the minimum number of swaps
(n - number of cycles of the permutation). Small n only."""
import itertools
import sys


def solve(a):
    n = len(a)
    best = None
    for perm in itertools.permutations(range(n)):
        if any((a[perm[i]] % 2) != (i % 2) for i in range(n)):
            continue
        seen = [False] * n
        cycles = 0
        for i in range(n):
            if not seen[i]:
                cycles += 1
                j = i
                while not seen[j]:
                    seen[j] = True
                    j = perm[j]
        swaps = n - cycles
        if best is None or swaps < best:
            best = swaps
    return -1 if best is None else best


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        out.append(solve(a))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
