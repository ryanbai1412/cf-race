import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        k = sum(1 for x in a if x < 0)
        b = [-abs(a[i]) if i < k else abs(a[i]) for i in range(n)]
        ok = all(b[i] <= b[i + 1] for i in range(n - 1))
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
