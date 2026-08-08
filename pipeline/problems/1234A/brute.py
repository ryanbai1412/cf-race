"""Independent brute force: scan candidate prices upward (small values only)."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    q = int(data[p])
    p += 1
    out = []
    for _ in range(q):
        n = int(data[p])
        p += 1
        a = list(map(int, data[p:p + n]))
        p += n
        s = sum(a)
        price = 0
        while price * n < s:
            price += 1
        out.append(price)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
