import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i].decode()
        cnt = Counter(s)
        pairs = sum(1 for v in cnt.values() if v >= 2)
        singles = sum(1 for v in cnt.values() if v == 1)
        out.append(pairs + singles // 2)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
