"""Independent brute force: fixpoint over states (set of player-1 cards).

State S wins for player 1 if he has a pure card choice x such that for every
opponent reply y the resulting state is already known winning (or he has won
outright). Iterated to a fixpoint, so cyclic play counts as not-winning.
"""
import sys


def solve(n, a):
    full = (1 << n) - 1
    start = 0
    for v in a:
        start |= 1 << (v - 1)
    win = {full}
    changed = True
    while changed:
        changed = False
        for s in range(1, full):
            if s in win:
                continue
            for i in range(n):
                if not s >> i & 1:
                    continue
                ok = True
                for j in range(n):
                    if s >> j & 1:
                        continue
                    ns = s | (1 << j) if i > j else s & ~(1 << i)
                    if ns == full:
                        continue
                    if ns == 0 or ns not in win:
                        ok = False
                        break
                if ok:
                    win.add(s)
                    changed = True
                    break
    return "YES" if start in win else "NO"


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p])
    p += 1
    out = []
    for _ in range(t):
        n, k1, k2 = map(int, data[p:p + 3])
        p += 3
        a = list(map(int, data[p:p + k1]))
        p += k1 + k2
        out.append(solve(n, a))
    sys.stdout.write("\n".join(out) + "\n")


main()
