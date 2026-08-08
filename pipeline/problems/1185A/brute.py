import sys


def main():
    a, b, c, d = map(int, sys.stdin.read().split())
    xs = sorted((a, b, c))
    # brute: try all final orderings within a small window around originals
    if max(xs) - min(xs) <= 40 and d <= 20:
        best = None
        lo = min(xs) - d * 2 - 5
        hi = max(xs) + d * 2 + 5
        for p in range(lo, hi + 1):
            for q in range(lo, hi + 1):
                for r in range(lo, hi + 1):
                    if abs(p - q) >= d and abs(q - r) >= d and abs(p - r) >= d:
                        cost = abs(p - xs[0]) + abs(q - xs[1]) + abs(r - xs[2])
                        if best is None or cost < best:
                            best = cost
        print(best)
    else:
        lo, mid, hi = xs
        print(max(0, d - (mid - lo)) + max(0, d - (hi - mid)))


main()
