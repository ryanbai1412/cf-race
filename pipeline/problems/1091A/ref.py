import sys


def main():
    y, b, r = map(int, sys.stdin.read().split())
    m = min(y, b - 1, r - 2)
    print(3 * m + 3)


main()
