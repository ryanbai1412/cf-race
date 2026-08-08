import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c = data[1 + 3 * i:4 + 3 * i]
        ok = all(cc == aa or cc == bb for aa, bb, cc in zip(a, b, c))
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
