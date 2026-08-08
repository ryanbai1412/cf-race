import sys

MOD = 10 ** 9 + 7


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    ns = [int(x) for x in data[1:1 + t]]
    mx = 2 * max(ns)
    fact = [1] * (mx + 1)
    for i in range(2, mx + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv2 = pow(2, MOD - 2, MOD)
    out = [str(fact[2 * n] * inv2 % MOD) for n in ns]
    sys.stdout.write("\n".join(out) + "\n")


main()
