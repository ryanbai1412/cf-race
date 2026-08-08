import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        d = [int(ch) for ch in s]
        out.append("YES" if d[0] + d[1] + d[2] == d[3] + d[4] + d[5] else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
