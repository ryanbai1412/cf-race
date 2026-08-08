import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, c = int(data[idx]), int(data[idx + 1])
        idx += 2
        cnt = Counter(data[idx : idx + n])
        idx += n
        out.append(str(sum(min(v, c) for v in cnt.values())))
    sys.stdout.write("\n".join(out) + "\n")


main()
