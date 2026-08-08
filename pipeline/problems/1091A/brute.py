"""Independent brute force: try every triple count, keep the best."""
import sys


def main():
    y, b, r = map(int, sys.stdin.read().split())
    best = 0
    for k in range(0, 101):  # k yellow, k+1 blue, k+2 red
        if k <= y and k + 1 <= b and k + 2 <= r:
            best = max(best, k + (k + 1) + (k + 2))
    print(best)


main()
