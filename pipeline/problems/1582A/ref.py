import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c = (int(x) for x in data[1 + 3 * i:4 + 3 * i])
        out.append(str((a + 2 * b + 3 * c) % 2))
    print("\n".join(out))


main()
