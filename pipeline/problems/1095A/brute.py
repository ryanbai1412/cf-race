"""Independent brute force: try every candidate s built from t's letters by
re-encrypting and comparing (search over lengths, verifying the encryption)."""
import sys


def encrypt(s):
    return "".join(c * (i + 1) for i, c in enumerate(s))


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    # greedily consume runs: s[i] must be the first char of the i-th block
    for m in range(1, 11):
        if m * (m + 1) // 2 != n:
            continue
        s = []
        pos = 0
        for i in range(1, m + 1):
            s.append(t[pos])
            pos += i
        cand = "".join(s)
        if encrypt(cand) == t:
            print(cand)
            return
    raise SystemExit("no answer")


main()
