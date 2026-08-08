import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + i])
        out.append((n - 1) // 2)
    print("\n".join(map(str, out)))


main()
