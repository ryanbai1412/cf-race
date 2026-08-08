"""Independent solution: re-sort the whole array for every query of type 2."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    a = list(map(int, data[2:2 + n]))
    p = 2 + n
    out = []
    for _ in range(q):
        typ = int(data[p]); v = int(data[p + 1]); p += 2
        if typ == 1:
            a[v - 1] = 1 - a[v - 1]
        else:
            out.append(str(sorted(a, reverse=True)[v - 1]))
    sys.stdout.write("\n".join(out) + "\n")


main()
