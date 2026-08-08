import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + i])
        # pile A: 2^n plus the n/2 - 1 smallest coins; pile B: the rest
        # |A - B| = 2^(n/2 + 1) - 2
        out.append(2 ** (n // 2 + 1) - 2)
    print("\n".join(map(str, out)))


main()
