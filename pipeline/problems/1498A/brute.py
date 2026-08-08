"""Independent brute: literal linear scan upward (small n only)."""
import sys


def digsum(x):
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        x = int(data[i])
        while gcd(x, digsum(x)) <= 1:
            x += 1
        out.append(x)
    print("\n".join(map(str, out)))


main()
