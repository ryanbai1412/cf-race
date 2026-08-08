import sys


def main():
    a = [int(x) for x in sys.stdin.read().split()]
    total = sum(a)
    ok = total % 2 == 0 and any(
        sum(a[i] for i in range(4) if mask >> i & 1) * 2 == total
        for mask in range(16))
    print("YES" if ok else "NO")


main()
