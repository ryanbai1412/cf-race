"""Independent check: sorted a, YES iff a0+a3==a1+a2 or a0+a1+a2==a3."""
import sys


def main():
    a = sorted(int(x) for x in sys.stdin.read().split())
    ok = (a[0] + a[3] == a[1] + a[2]) or (a[0] + a[1] + a[2] == a[3])
    print("YES" if ok else "NO")


main()
