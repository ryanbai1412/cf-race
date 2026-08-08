import sys
from itertools import combinations


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        k = sum(1 for x in a if x < 0)
        vals = [abs(x) for x in a]
        ok = False
        # the op preserves the number of negatives; any placement reachable
        for neg_idx in combinations(range(n), k):
            b = [-vals[i] if i in neg_idx else vals[i] for i in range(n)]
            if all(b[i] <= b[i + 1] for i in range(n - 1)):
                ok = True
                break
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
