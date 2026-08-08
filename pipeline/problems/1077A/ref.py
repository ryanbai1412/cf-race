import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, k = (int(x) for x in data[1 + 3 * i:4 + 3 * i])
        out.append((k + 1) // 2 * a - (k // 2) * b)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
