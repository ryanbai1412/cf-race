import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); m = int(data[p + 1]); p += 2
        s = sum(int(x) for x in data[p:p + n]); p += n
        out.append("YES" if s == m else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
