import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = list(map(int, data[p:p + n])); p += n
        ans = 0
        for i in range(n - 1):
            lo, hi = min(a[i], a[i + 1]), max(a[i], a[i + 1])
            while lo * 2 < hi:
                lo *= 2
                ans += 1
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
