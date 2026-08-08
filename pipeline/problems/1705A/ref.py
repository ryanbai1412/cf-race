import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n, x = int(data[pos]), int(data[pos + 1]); pos += 2
        h = sorted(int(v) for v in data[pos:pos + 2 * n]); pos += 2 * n
        ok = all(h[i + n] - h[i] >= x for i in range(n))
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
