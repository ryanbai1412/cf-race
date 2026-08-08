import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        odd_ok = all(a[i] % 2 == a[0] % 2 for i in range(0, n, 2))
        even_ok = all(a[i] % 2 == a[1] % 2 for i in range(1, n, 2))
        out.append("YES" if odd_ok and even_ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
