"""Independent solution: literally rotate the matrix four times."""
import sys


def beautiful(m):
    return m[0][0] < m[0][1] and m[1][0] < m[1][1] and m[0][0] < m[1][0] and m[0][1] < m[1][1]


def rotate(m):
    return [[m[1][0], m[0][0]], [m[1][1], m[0][1]]]


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        m = [[int(data[pos]), int(data[pos + 1])], [int(data[pos + 2]), int(data[pos + 3])]]
        pos += 4
        ok = False
        for _ in range(4):
            if beautiful(m):
                ok = True
            m = rotate(m)
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
