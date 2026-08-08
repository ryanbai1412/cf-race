"""Independent solution: repeatedly overwrite the largest element with the
smallest achievable sum of two other elements, stop when stuck."""
import sys


def solve(n, d, a):
    a = list(a)
    for _ in range(3 * n + 10):
        i = max(range(n), key=lambda j: a[j])
        if a[i] <= d:
            return "YES"
        rest = sorted(a[:i] + a[i + 1:])
        s = rest[0] + rest[1]
        if s >= a[i]:
            return "NO"
        a[i] = s
    return "NO"


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); d = int(data[p + 1]); p += 2
        a = list(map(int, data[p:p + n])); p += n
        out.append(solve(n, d, a))
    sys.stdout.write("\n".join(out) + "\n")


main()
