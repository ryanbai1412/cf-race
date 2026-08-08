import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        v = [int(x) for x in data[pos:pos + 4]]
        pos += 4
        # beautiful means the min sits at (0,0) and the max at (1,1);
        # rotations move both, so min and max must be on the same diagonal
        lo = v.index(min(v))
        hi = v.index(max(v))
        ok = {lo, hi} in ({0, 3}, {1, 2})
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
