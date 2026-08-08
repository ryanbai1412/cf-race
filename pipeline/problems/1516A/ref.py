import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n, k = int(data[pos]), int(data[pos + 1]); pos += 2
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        for i in range(n - 1):
            if k <= 0:
                break
            d = min(k, a[i])
            a[i] -= d
            a[-1] += d
            k -= d
        out.append(" ".join(map(str, a)))
    sys.stdout.write("\n".join(out) + "\n")


main()
