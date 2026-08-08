import sys


def main():
    n, s = map(int, sys.stdin.read().split())
    print((s + n - 1) // n)


main()
