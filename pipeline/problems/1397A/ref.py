import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        c = Counter()
        for _ in range(n):
            c.update(next(it))
        out.append("YES" if all(v % n == 0 for v in c.values()) else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
