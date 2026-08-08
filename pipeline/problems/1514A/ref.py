import math
import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos : pos + n]]
        pos += n
        ans = any(math.isqrt(x) ** 2 != x for x in a)
        out.append("YES" if ans else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
