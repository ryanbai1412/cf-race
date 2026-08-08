import sys
from itertools import product


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1 : 1 + n]))
    best = None
    for mask in product([1, -1], repeat=n):
        v = sum(s * x for s, x in zip(mask, a))
        best = v if best is None else max(best, v)
    print(best)


main()
