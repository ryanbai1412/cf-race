import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    k = int(data[p])
    p += 1
    out = []
    for _ in range(k):
        n = int(data[p])
        p += 1
        a = sorted(map(int, data[p:p + n]), reverse=True)
        p += n
        ans = 0
        for i, v in enumerate(a, 1):
            if v >= i:
                ans = i
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
