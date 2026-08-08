import sys


def main():
    l, r, a = map(int, sys.stdin.read().split())
    best = 0
    # al ambidexters play left, ar play right
    for al in range(a + 1):
        for ar in range(a - al + 1):
            left = l + al
            right = r + ar
            best = max(best, 2 * min(left, right))
    print(best)


main()
