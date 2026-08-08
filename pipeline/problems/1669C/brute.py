import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) % 2 for x in data[pos:pos + n]]; pos += n
        ok = False
        # only parity of op counts matters: try (x, y) in {0,1}^2
        for x in (0, 1):
            for y in (0, 1):
                b = [(a[i] + (x if i % 2 == 0 else y)) % 2 for i in range(n)]
                if len(set(b)) == 1:
                    ok = True
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
