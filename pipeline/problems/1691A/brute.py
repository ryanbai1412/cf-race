"""Independent brute force: try all subsets (n <= ~15)."""
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
        best = n  # remove everything (vacuously fine)
        for keep in range(n, 0, -1):
            found = False
            for idx in combinations(range(n), keep):
                sub = [a[i] for i in idx]
                if all((sub[i] + sub[i + 1]) % 2 == 0 for i in range(len(sub) - 1)):
                    found = True
                    break
            if found:
                best = n - keep
                break
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
