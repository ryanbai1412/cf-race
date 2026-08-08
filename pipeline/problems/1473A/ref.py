import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); d = int(data[p + 1]); p += 2
        a = list(map(int, data[p:p + n])); p += n
        a.sort()
        out.append("YES" if a[-1] <= d or a[0] + a[1] <= d else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
