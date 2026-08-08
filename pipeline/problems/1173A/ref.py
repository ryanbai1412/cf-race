import sys


def main():
    x, y, z = map(int, sys.stdin.read().split())
    res = set()
    for up in range(z + 1):
        a = x + up
        b = y + (z - up)
        res.add("+" if a > b else ("-" if a < b else "0"))
    print(next(iter(res)) if len(res) == 1 else "?")


main()
