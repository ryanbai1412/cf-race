import math
import sys


def solve(k):
    m = math.isqrt(k - 1) + 1  # layer index: (m-1)^2 < k <= m^2
    off = k - (m - 1) * (m - 1)
    if off <= m:
        return m if False else (off, m)
    return (m, 2 * m - off)


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        r, c = solve(int(data[i + 1]))
        out.append(f"{r} {c}")
    sys.stdout.write("\n".join(out) + "\n")


main()
