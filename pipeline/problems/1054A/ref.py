import sys


def main():
    x, y, z, t1, t2, t3 = map(int, sys.stdin.read().split())
    stairs = abs(x - y) * t1
    elevator = (abs(z - x) + abs(x - y)) * t2 + 3 * t3
    print("YES" if elevator <= stairs else "NO")


main()
