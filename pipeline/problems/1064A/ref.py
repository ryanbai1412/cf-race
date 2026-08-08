import sys


def main():
    a, b, c = sorted(map(int, sys.stdin.read().split()))
    print(max(0, c - a - b + 1))


main()
