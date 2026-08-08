"""Independent solution: search over how many extra crystals of each colour to buy
(only valid for small inputs; used for stress testing)."""
import sys


def main():
    a, b = map(int, sys.stdin.readline().split())
    x, y, z = map(int, sys.stdin.readline().split())
    best = None
    for extra_y in range(0, 2 * x + y + 1):
        for extra_b in range(0, y + 3 * z + 1):
            ty, tb = a + extra_y, b + extra_b
            # make x yellow balls, y green balls, z blue balls
            if ty >= 2 * x and tb >= 3 * z and ty - 2 * x >= y and tb - 3 * z >= y:
                s = extra_y + extra_b
                if best is None or s < best:
                    best = s
    print(best)


main()
