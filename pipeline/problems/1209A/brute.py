"""Independent brute force: exhaustive partition search (small n only)."""
import sys


def solve(a):
    a = sorted(a)  # ascending: each group's minimum is its first element
    best = [len(a)]

    def rec(i, groups):
        if len(groups) >= best[0]:
            return
        if i == len(a):
            best[0] = len(groups)
            return
        v = a[i]
        for g in groups:
            if v % g[0] == 0:
                g.append(v)
                rec(i + 1, groups)
                g.pop()
        groups.append([v])
        rec(i + 1, groups)
        groups.pop()

    rec(0, [])
    return best[0]


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    print(solve(a))


main()
