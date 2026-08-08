import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p])
    p += 1
    out = []
    for _ in range(t):
        n, k1, k2 = map(int, data[p:p + 3])
        p += 3
        a = list(map(int, data[p:p + k1]))
        p += k1
        p += k2
        out.append("YES" if n in a else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
