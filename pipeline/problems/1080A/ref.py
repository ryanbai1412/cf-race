import sys


def main():
    n, k = map(int, sys.stdin.read().split())
    print(sum((n * c + k - 1) // k for c in (2, 5, 8)))


main()
