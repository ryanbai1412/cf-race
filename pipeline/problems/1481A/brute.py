"""Independent solution: DP over the set of positions reachable by any
subsequence of the prefix (feasible only for tiny |s|)."""
import sys


def solve(px, py, s):
    cur = {(0, 0)}
    step = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}
    for ch in s:
        dx, dy = step[ch]
        cur |= {(x + dx, y + dy) for x, y in cur}
    return "YES" if (px, py) in cur else "NO"


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        px = int(data[p]); py = int(data[p + 1]); p += 2
        s = data[p].decode(); p += 1
        out.append(solve(px, py, s))
    sys.stdout.write("\n".join(out) + "\n")


main()
