"""Independent brute force: try all (h, w); Michael wins iff every h x w
subrectangle has the same maximum."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        g = []
        for i in range(n):
            g.append([int(x) for x in data[pos:pos + m]])
            pos += m
        best = n * m
        for h in range(1, n + 1):
            for w in range(1, m + 1):
                if h * w >= best:
                    continue
                maxes = set()
                for a in range(n - h + 1):
                    for b in range(m - w + 1):
                        mx = max(g[i][j] for i in range(a, a + h)
                                 for j in range(b, b + w))
                        maxes.add(mx)
                if len(maxes) == 1:
                    best = h * w
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
