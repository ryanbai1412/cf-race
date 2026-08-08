import sys


def main():
    a, b, c, d, e, f = (int(x) for x in sys.stdin.read().split())
    best = 0
    for k in range(0, min(a, d) + 1):
        for m in range(0, min(b, c, d - k) + 1):
            best = max(best, k * e + m * f)
    print(best)


main()
