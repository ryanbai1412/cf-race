import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, x, y = (int(v) for v in data[1 + 4 * i:5 + 4 * i])
        out.append(max(x * b, (a - x - 1) * b, y * a, (b - y - 1) * a))
    print("\n".join(map(str, out)))


main()
