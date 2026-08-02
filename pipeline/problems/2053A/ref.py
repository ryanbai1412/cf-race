import sys

def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        ok = any(2 * min(a[i], a[i + 1]) > max(a[i], a[i + 1])
                 for i in range(n - 1))
        out.append("YES" if ok else "NO")
    print("\n".join(out))

main()
