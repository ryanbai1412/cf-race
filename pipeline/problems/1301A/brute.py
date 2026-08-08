import sys
from itertools import product


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    for i in range(t):
        a, b, c = data[1 + 3 * i:4 + 3 * i]
        n = len(a)
        ok = False
        for mask in product((0, 1), repeat=n):
            la, lb, lc = list(a), list(b), list(c)
            for j, m in enumerate(mask):
                if m == 0:
                    la[j], lc[j] = lc[j], la[j]
                else:
                    lb[j], lc[j] = lc[j], lb[j]
            if la == lb:
                ok = True
                break
        print("YES" if ok else "NO")


main()
