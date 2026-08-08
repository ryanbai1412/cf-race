import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, m, r, c = (int(x) for x in data[idx : idx + 4])
        idx += 4
        grid = data[idx : idx + n]
        idx += n
        grid = [g.decode() for g in grid]
        if grid[r - 1][c - 1] == "B":
            ans = 0
        elif "B" in grid[r - 1] or any(row[c - 1] == "B" for row in grid):
            ans = 1
        elif any("B" in row for row in grid):
            ans = 2
        else:
            ans = -1
        out.append(str(ans))
    print("\n".join(out))


main()
