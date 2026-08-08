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
        a = sorted(map(int, data[p:p + n]))
        p += n
        out.append(2 if any(y - x == 1 for x, y in zip(a, a[1:])) else 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
