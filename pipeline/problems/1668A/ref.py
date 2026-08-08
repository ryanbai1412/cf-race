import sys


def solve(n, m):
    if n > m:
        n, m = m, n
    a, b = n - 1, m - 1
    if a == 0:
        if b == 0:
            return 0
        if b == 1:
            return 1
        return -1
    e = b - a
    return a + b + 2 * (e // 2)


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
