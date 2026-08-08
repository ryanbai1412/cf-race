import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = sorted(map(int, data[pos:pos + n])); pos += n
        ok = all(a[i + 1] - a[i] <= 1 for i in range(n - 1))
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")

main()
