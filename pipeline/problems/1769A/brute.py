"""Independent solution: closed form b_i = i + max_{j<=i} (a_j - 2j)."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    out = []
    best = None
    for i in range(1, n + 1):
        cand = a[i - 1] - 2 * i
        best = cand if best is None else max(best, cand)
        out.append(best + i)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
