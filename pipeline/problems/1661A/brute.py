import sys
from itertools import product


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        b = [int(x) for x in data[pos:pos + n]]; pos += n
        best = None
        for mask in product([0, 1], repeat=n):
            aa = [b[i] if mask[i] else a[i] for i in range(n)]
            bb = [a[i] if mask[i] else b[i] for i in range(n)]
            s = sum(abs(aa[i] - aa[i + 1]) + abs(bb[i] - bb[i + 1]) for i in range(n - 1))
            if best is None or s < best:
                best = s
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
