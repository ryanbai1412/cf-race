import sys

n = int(sys.stdin.read().split()[0])
cells = {(0, 0)}
for _ in range(n - 1):
    new = set(cells)
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new.add((x + dx, y + dy))
    cells = new
print(len(cells))
