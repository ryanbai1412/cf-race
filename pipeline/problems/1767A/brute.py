"""Independent solution: a valid cut must pass through a vertex and strictly
separate the other two vertices."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        p = []
        for _ in range(3):
            p.append((int(data[pos]), int(data[pos + 1])))
            pos += 2
        ok = False
        for coord in (0, 1):
            for i in range(3):
                c = p[i][coord]
                others = [p[j][coord] for j in range(3) if j != i]
                if (others[0] - c) * (others[1] - c) < 0:
                    ok = True
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
