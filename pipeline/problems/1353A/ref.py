import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n, m = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        if n == 1:
            out.append(0)
        elif n == 2:
            out.append(m)
        else:
            out.append(2 * m)
    print("\n".join(map(str, out)))


main()
