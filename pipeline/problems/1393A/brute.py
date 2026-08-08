"""Independent solution: simulate the game on a real grid (small n only).

The chess coloring is fixed up to which parity class each pony owns, and a
block of one color can only become placeable after a block of the other color
is placed, so turns alternate. For each of the two parity assignments, greedily
place every currently-placeable cell of the active color each turn.
"""
import sys


def simulate(n, start_parity):
    filled = [[False] * n for _ in range(n)]
    remaining = n * n
    turns = 0
    parity = start_parity
    while remaining:
        placed = []
        for i in range(n):
            for j in range(n):
                if filled[i][j] or (i + j) % 2 != parity:
                    continue
                touches = i == 0 or j == 0 or i == n - 1 or j == n - 1
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    x, y = i + di, j + dj
                    if 0 <= x < n and 0 <= y < n and filled[x][y]:
                        touches = True
                if touches:
                    placed.append((i, j))
        if not placed:
            return None
        for i, j in placed:
            filled[i][j] = True
        remaining -= len(placed)
        turns += 1
        parity ^= 1
    return turns


def solve(n):
    return min(x for x in (simulate(n, 0), simulate(n, 1)) if x is not None)


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = [str(solve(int(data[i]))) for i in range(1, t + 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
