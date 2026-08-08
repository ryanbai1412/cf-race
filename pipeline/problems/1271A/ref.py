import sys


def main():
    a, b, c, d, e, f = (int(x) for x in sys.stdin.read().split())
    best = 0
    for k in range(0, min(a, d) + 1):
        best = max(best, k * e + min(b, c, d - k) * f)
    print(best)


main()
