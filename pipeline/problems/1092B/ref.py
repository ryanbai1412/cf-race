import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = sorted(map(int, data[1:1 + n]))
    print(sum(a[i + 1] - a[i] for i in range(0, n, 2)))


main()
