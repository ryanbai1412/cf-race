"""Independent solution: literally simulate the k operations (small k only)."""
import sys


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        for _ in range(k):
            d = max(a)
            a = [d - x for x in a]
        out.append(" ".join(map(str, a)))
    sys.stdout.write("\n".join(out) + "\n")


main()
