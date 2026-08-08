"""Independent solution: for small n, brute-force every candidate a and keep
the one maximizing d (verified unique for n <= 10)."""
import sys
from itertools import product


def d_of(c):
    out = []
    for ch in c:
        if not out or out[-1] != ch:
            out.append(ch)
    return "".join(out)


def solve(b):
    n = len(b)
    best = -1
    besta = None
    for a in product("01", repeat=n):
        c = "".join(str(int(x) + int(y)) for x, y in zip(a, b))
        v = int(d_of(c))
        if v > best:
            best = v
            besta = "".join(a)
    return besta


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        p += 1
        b = data[p].decode(); p += 1
        out.append(solve(b))
    sys.stdout.write("\n".join(out) + "\n")


main()
