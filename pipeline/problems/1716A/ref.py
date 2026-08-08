import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        out.append(2 if n == 1 else (n + 2) // 3)
    print("\n".join(map(str, out)))


main()
