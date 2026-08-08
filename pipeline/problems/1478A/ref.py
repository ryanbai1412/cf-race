import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = data[p:p + n]; p += n
        out.append(str(max(Counter(a).values())))
    sys.stdout.write("\n".join(out) + "\n")


main()
