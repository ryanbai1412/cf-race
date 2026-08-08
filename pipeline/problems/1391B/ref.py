import sys


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        g = [next(it) for _ in range(n)]
        cnt = 0
        for j in range(m - 1):
            if g[n - 1][j] == "D":
                cnt += 1
        for i in range(n - 1):
            if g[i][m - 1] == "R":
                cnt += 1
        out.append(str(cnt))
    sys.stdout.write("\n".join(out) + "\n")


main()
