"""Independent alternative: process heights in a plain loop over 1..h with a
list of stones instead of a dict lookup."""
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    w, h, u1, d1, u2, d2 = data[:6]
    stones = [(d1, u1), (d2, u2)]
    cur = w
    for height in range(h, 0, -1):
        cur += height
        for d, u in stones:
            if d == height:
                cur -= u
                if cur < 0:
                    cur = 0
    print(cur)


main()
