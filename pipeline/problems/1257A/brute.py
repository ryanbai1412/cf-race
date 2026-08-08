"""Independent brute force: BFS over (posA, posB) states, each adjacent swap
costing one operation; only swaps involving a rival can change the state."""
import sys
from collections import deque


def solve(n, x, a, b):
    start = (a, b)
    dist = {start: 0}
    q = deque([start])
    best = abs(a - b)
    while q:
        p, s = q.popleft()
        d = dist[(p, s)]
        if d == x:
            continue
        moves = []
        for cur, other in ((p, s), (s, p)):
            for nxt in (cur - 1, cur + 1):
                if 1 <= nxt <= n:
                    if nxt == other:  # swapping the two rivals with each other
                        moves.append((other, cur) if cur == p else (cur, other))
                    else:
                        moves.append((nxt, other) if cur == p else (other, nxt))
        for st in moves:
            if st not in dist:
                dist[st] = d + 1
                best = max(best, abs(st[0] - st[1]))
                q.append(st)
    return best


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n, x, a, b = map(int, data[1 + 4 * i:5 + 4 * i])
        out.append(solve(n, x, a, b))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
