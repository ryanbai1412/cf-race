import sys


def solve(n, m, s):
    INF = float("inf")
    dl = [INF] * n
    dr = [INF] * n
    last = -INF
    for i, c in enumerate(s):
        if c == "1":
            last = i
        dl[i] = i - last
    last = INF
    for i in range(n - 1, -1, -1):
        if s[i] == "1":
            last = i
        dr[i] = last - i
    res = []
    for i in range(n):
        if s[i] == "1":
            res.append("1")
        elif dl[i] != dr[i] and min(dl[i], dr[i]) <= m:
            res.append("1")
        else:
            res.append("0")
    return "".join(res)


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    pos = 1
    for _ in range(t):
        n, m = int(data[pos]), int(data[pos + 1])
        s = data[pos + 2]
        pos += 3
        out.append(solve(n, m, s))
    sys.stdout.write("\n".join(out) + "\n")


main()
