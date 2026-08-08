import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        h = int(data[1 + 2 * i])
        m = int(data[2 + 2 * i])
        out.append(1440 - h * 60 - m)
    print("\n".join(map(str, out)))


main()
