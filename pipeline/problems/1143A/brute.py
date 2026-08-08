"""Independent brute force: scan prefixes and test both exits explicitly."""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    tot0 = a.count(0)
    tot1 = a.count(1)
    c0 = c1 = 0
    for k in range(n):
        if a[k] == 0:
            c0 += 1
        else:
            c1 += 1
        if c0 == tot0 or c1 == tot1:
            print(k + 1)
            return


main()
