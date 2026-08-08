import sys


def main():
    x, y, z = map(int, sys.stdin.read().split())
    lo = x - y - z
    hi = x - y + z
    if lo > 0:
        print("+")
    elif hi < 0:
        print("-")
    elif lo == 0 and hi == 0:
        print("0")
    else:
        print("?")


main()
