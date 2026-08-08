"""Independent brute force: bounded BFS over op sequences (tiny inputs).

For k >= 2 an operation can never increase the too-tall count, so a bounded
search finds the true optimum. For k == 1 the optimum needs unboundedly many
ops; instead we build the explicit optimal construction (pump every other
interior pile far above its neighbours) and count the result.
"""
import sys


def count_tall(a):
    return sum(a[i] > a[i - 1] + a[i + 1] for i in range(1, len(a) - 1))


def solve(n, k, a, depth=6):
    if k == 1:
        b = list(a)
        big = sum(a) + 10**9
        for i in range(1, n - 1, 2):
            b[i] = big
            big += b[i - 1] + b[i + 1] + 1
        # re-pump until stable (neighbours never change for k == 1)
        for i in range(1, n - 1, 2):
            b[i] = b[i - 1] + b[i + 1] + 1
        return count_tall(b)
    best = count_tall(a)
    frontier = {tuple(a)}
    for _ in range(depth):
        nxt = set()
        for st in frontier:
            for l in range(0, n - k + 1):
                nb = list(st)
                for i in range(l, l + k):
                    nb[i] += 1
                tb = tuple(nb)
                if tb not in nxt:
                    nxt.add(tb)
                    best = max(best, count_tall(nb))
        frontier = nxt
        if len(frontier) > 20000:
            break
    return best


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        out.append(solve(n, k, a))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
