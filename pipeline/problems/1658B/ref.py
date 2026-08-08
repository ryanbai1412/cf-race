import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    fact = [1] * 501
    for i in range(1, 501):
        fact[i] = fact[i - 1] * i % MOD
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        if n % 2 == 1:
            out.append("0")
        else:
            f = fact[n // 2]
            out.append(str(f * f % MOD))
    sys.stdout.write("\n".join(out) + "\n")


main()
