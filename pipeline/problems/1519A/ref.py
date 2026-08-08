import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    pos = 1
    for _ in range(t):
        r, b, d = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        lo, hi = min(r, b), max(r, b)
        out.append("YES" if hi <= lo * (d + 1) else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
