import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n, m = int(data[pos]), int(data[pos + 1]); pos += 2
        a = [int(v) for v in data[pos:pos + n]]; pos += n
        s = ["B"] * m
        for ai in a:
            i, j = ai - 1, m - ai
            lo, hi = min(i, j), max(i, j)
            if s[lo] == "B":
                s[lo] = "A"
            else:
                s[hi] = "A"
        out.append("".join(s))
    print("\n".join(out))


main()
