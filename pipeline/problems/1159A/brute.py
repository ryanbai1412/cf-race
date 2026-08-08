"""Independent brute force: try every starting pile size, keep valid minimum."""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    best = None
    for start in range(n + 1):
        cur = start
        ok = True
        for ch in s:
            if ch == "+":
                cur += 1
            else:
                if cur == 0:
                    ok = False
                    break
                cur -= 1
        if ok and (best is None or cur < best):
            best = cur
    print(best)


main()
