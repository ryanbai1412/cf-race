import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, m = int(data[idx]), int(data[idx + 1])
        idx += 2 + 2 * m
        out.append("YES" if m < n else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
