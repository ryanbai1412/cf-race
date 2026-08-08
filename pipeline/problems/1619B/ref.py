import sys


def iroot(n, k):
    r = int(round(n ** (1.0 / k)))
    while r ** k > n:
        r -= 1
    while (r + 1) ** k <= n:
        r += 1
    return r


data = sys.stdin.read().split()
t = int(data[0])
out = []
for i in range(1, t + 1):
    n = int(data[i])
    out.append(str(iroot(n, 2) + iroot(n, 3) - iroot(n, 6)))
print("\n".join(out))
