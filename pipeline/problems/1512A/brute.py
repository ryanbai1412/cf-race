"""Independent second implementation using Counter."""
import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos : pos + n]
        pos += n
        rare = min(Counter(a).items(), key=lambda kv: kv[1])[0]
        out.append(a.index(rare) + 1)
    print("\n".join(map(str, out)))


main()
