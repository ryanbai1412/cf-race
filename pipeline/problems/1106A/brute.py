"""Independent brute force: for every cell, test the 5 required positions with
explicit bounds checks (no assumption about the interior loop range)."""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    g = data[1:1 + n]
    cnt = 0
    for i in range(n):
        for j in range(n):
            ok = True
            for di, dj in ((0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                ni, nj = i + di, j + dj
                if not (0 <= ni < n and 0 <= nj < n) or g[ni][nj] != 'X':
                    ok = False
                    break
            if ok:
                cnt += 1
    print(cnt)


main()
