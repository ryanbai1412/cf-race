"""Independent brute force for small ranges: try every prime p <= r.

For a fixed prime p, each operation can reduce the count of elements not
divisible by p by at most one (and merging a non-divisible with anything
divisible achieves that), so the minimum ops to make gcd % p == 0 is the
count of non-divisible elements — unless no element is divisible by p and
the array has more than one element merged down to a single non-divisible
product, which never helps.
"""
import sys


def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = [False] * len(sieve[i * i :: i])
    return [i for i, v in enumerate(sieve) if v]


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        l, r, k = (int(x) for x in data[idx : idx + 3])
        idx += 3
        if l == r:
            print("YES" if l > 1 else "NO")
            continue
        ans = "NO"
        for p in primes_up_to(r):
            div = r // p - (l - 1) // p
            if div == 0:
                continue
            nondiv = (r - l + 1) - div
            if nondiv <= k:
                ans = "YES"
                break
        print(ans)


main()
