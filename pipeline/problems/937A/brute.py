"""Independent solution: enumerate every threshold and collect the distinct
award sets it produces."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    seen = set()
    for thr in range(1, 601):
        awarded = frozenset(i for i in range(n) if a[i] >= thr)
        if awarded and all(a[i] > 0 for i in awarded):
            seen.add(awarded)
    print(len(seen))


main()
