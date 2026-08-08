import sys


def main():
    l, r, a = map(int, sys.stdin.read().split())
    lo, hi = min(l, r), max(l, r)
    t = min(a, hi - lo)
    lo += t
    a -= t
    print(2 * (lo + a // 2))


main()
