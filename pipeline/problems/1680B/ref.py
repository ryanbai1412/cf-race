import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    out = []
    for _ in range(t):
        n, m = int(data[idx]), int(data[idx + 1])
        idx += 2
        grid = data[idx : idx + n]
        idx += n
        rows = [i for i in range(n) if "R" in grid[i]]
        cols = [j for j in range(m) if any(grid[i][j] == "R" for i in range(n))]
        out.append("YES" if grid[min(rows)][min(cols)] == "R" else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
