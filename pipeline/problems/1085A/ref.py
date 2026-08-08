import sys


def main():
    t = sys.stdin.readline().strip()
    lo, hi = 0, len(t) - 1
    res = []
    for i in range(len(t), 1, -1):
        if i % 2 == 0:
            res.append(t[hi])
            hi -= 1
        else:
            res.append(t[lo])
            lo += 1
    res.append(t[lo])
    print("".join(reversed(res)))


main()
