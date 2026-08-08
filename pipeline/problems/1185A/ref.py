import sys


def main():
    a, b, c, d = map(int, sys.stdin.read().split())
    lo, mid, hi = sorted((a, b, c))
    print(max(0, d - (mid - lo)) + max(0, d - (hi - mid)))


main()
