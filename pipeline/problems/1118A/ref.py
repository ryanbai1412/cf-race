import sys


def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    out = []
    for i in range(q):
        n, a, b = (int(v) for v in data[1 + 3 * i:4 + 3 * i])
        out.append(n // 2 * min(b, 2 * a) + n % 2 * a)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
