import sys


def main():
    a, b = map(int, sys.stdin.readline().split())
    x, y, z = map(int, sys.stdin.readline().split())
    need_y = 2 * x + y
    need_b = y + 3 * z
    print(max(0, need_y - a) + max(0, need_b - b))


main()
