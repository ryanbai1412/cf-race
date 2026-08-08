import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        l = int(data[1 + 2 * i]); r = int(data[2 + 2 * i])
        out.append("YES" if 2 * l > r else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
