import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        best = None
        bi = bj = 0
        for i in range(n):
            for j in range(m):
                v = int(data[pos]); pos += 1
                if best is None or v > best:
                    best, bi, bj = v, i, j
        h = max(bi + 1, n - bi)
        w = max(bj + 1, m - bj)
        out.append(h * w)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
