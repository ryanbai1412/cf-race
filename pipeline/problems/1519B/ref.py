import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    pos = 1
    for _ in range(t):
        n, m, k = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        out.append("YES" if k == n * m - 1 else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
