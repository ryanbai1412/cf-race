import sys


def main():
    n, x, y = map(int, sys.stdin.read().split())
    white = max(x - 1, y - 1)
    black = max(n - x, n - y)
    print("White" if white <= black else "Black")


main()
