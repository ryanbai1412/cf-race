import sys
from itertools import groupby


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i].decode()
        ok = all(len(list(g)) >= 2 for _, g in groupby(s))
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
