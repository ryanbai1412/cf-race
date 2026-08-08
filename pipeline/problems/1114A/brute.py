"""Independent brute force: enumerate every distribution (small inputs only)."""
import sys


def main():
    x, y, z, a, b, c = map(int, sys.stdin.read().split())
    for ga in range(a + 1):  # green to Andrew
        if ga < x:
            continue
        for gd in range(a - ga + 1):  # green to Dmitry
            for pd in range(b + 1):  # purple to Dmitry
                if gd + pd < y:
                    continue
                left = (a - ga - gd) + (b - pd) + c
                if left >= z:
                    print("YES")
                    return
    print("NO")


main()
