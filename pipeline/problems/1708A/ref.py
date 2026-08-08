import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(v) for v in data[pos:pos + n]]; pos += n
        ok = all(v % a[0] == 0 for v in a)
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
