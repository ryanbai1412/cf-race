"""Independent brute: try all 2^n server assignments, simulate votes."""
import sys


def solve(r):
    n = len(r)
    best = 0
    for mask in range(1 << n):
        up = [0, 0]
        down = [0, 0]
        for i, typ in enumerate(r):
            s = (mask >> i) & 1
            if typ == 1:
                up[s] += 1
            elif typ == 2:
                down[s] += 1
            else:
                if down[s] > up[s]:
                    down[s] += 1
                else:
                    up[s] += 1
        best = max(best, up[0] + up[1])
    return best


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        r = [int(x) for x in data[idx : idx + n]]
        idx += n
        out.append(solve(r))
    print("\n".join(map(str, out)))


main()
