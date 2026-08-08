"""Independent brute: max domino matching among white / black cells via DFS."""
import sys
sys.setrecursionlimit(10000)


def max_match(cells):
    cells = sorted(cells)
    s = set(cells)

    def rec(cs):
        if not cs:
            return 0
        c = cs[0]
        rest = cs[1:]
        best = rec(rest)
        for d in ((0, 1), (1, 0)):
            nb = (c[0] + d[0], c[1] + d[1])
            if nb in s and nb in rest:
                r2 = [x for x in rest if x != nb]
                best = max(best, 1 + rec(r2))
        return best

    return rec(cells)


def solve(n, k1, k2, w, b):
    white = [(0, j) for j in range(k1)] + [(1, j) for j in range(k2)]
    black = [(0, j) for j in range(k1, n)] + [(1, j) for j in range(k2, n)]
    return "YES" if w <= max_match(white) and b <= max_match(black) else "NO"


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, k1, k2, w, b = (int(x) for x in data[idx : idx + 5])
        idx += 5
        out.append(solve(n, k1, k2, w, b))
    print("\n".join(out))


main()
