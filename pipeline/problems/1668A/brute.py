import sys
from collections import deque


def solve(n, m):
    # BFS over (r, c, lastdir); lastdir 0..3 or 4 (none)
    start = (0, 0, 4)
    if n == 1 and m == 1:
        return 0
    dist = {start: 0}
    q = deque([start])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c, ld = q.popleft()
        d0 = dist[(r, c, ld)]
        for k, (dr, dc) in enumerate(dirs):
            if k == ld:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and (nr, nc, k) not in dist:
                dist[(nr, nc, k)] = d0 + 1
                if nr == n - 1 and nc == m - 1:
                    return d0 + 1
                q.append((nr, nc, k))
    return -1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i])
        m = int(data[2 + 2 * i])
        out.append(str(solve(n, m)))
    sys.stdout.write("\n".join(out) + "\n")


main()
