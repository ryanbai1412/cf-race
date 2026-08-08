"""Independent brute force: try every k from 0..max(a)."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        b = [int(x) for x in data[pos:pos + n]]; pos += n
        ans = "NO"
        for k in range(0, max(a) + 1 if a else 1):
            if all(max(ai - k, 0) == bi for ai, bi in zip(a, b)):
                ans = "YES"
                break
        out.append(ans)
    sys.stdout.write("\n".join(out) + "\n")


main()
