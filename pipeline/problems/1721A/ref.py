import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = data[1 + 2 * i] + data[2 + 2 * i]
        out.append(len(set(s)) - 1)
    print("\n".join(map(str, out)))


main()
