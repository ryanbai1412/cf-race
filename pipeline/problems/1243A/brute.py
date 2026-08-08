"""Independent brute force: for each side s, count planks of height >= s."""
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
        a = list(map(int, data[p:p + n]))
        p += n
        ans = 0
        for s in range(1, n + 1):
            if sum(1 for v in a if v >= s) >= s:
                ans = max(ans, s)
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
