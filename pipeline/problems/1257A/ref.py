import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n, x, a, b = map(int, data[1 + 4 * i:5 + 4 * i])
        out.append(min(n - 1, abs(a - b) + x))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
