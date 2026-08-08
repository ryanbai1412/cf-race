import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); x = int(data[p + 1]); p += 2
        a = [int(v) for v in data[p:p + n]]; p += n
        b = [int(v) for v in data[p:p + n]]; p += n
        ok = all(a[i] + b[n - 1 - i] <= x for i in range(n))
        out.append("Yes" if ok else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
