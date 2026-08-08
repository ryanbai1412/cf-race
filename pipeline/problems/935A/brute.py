"""Independent solution: try every possible number of leaders directly."""
import sys


def main():
    n = int(sys.stdin.readline())
    print(sum(1 for l in range(1, n) if (n - l) % l == 0))


main()
