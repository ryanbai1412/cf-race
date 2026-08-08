import sys


def main():
    x, y, z, a, b, c = map(int, sys.stdin.read().split())
    if a < x:
        print("NO")
        return
    a -= x
    if a + b < y:
        print("NO")
        return
    rest = a + b - y
    print("YES" if rest + c >= z else "NO")


main()
