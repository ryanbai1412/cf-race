import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        p = [int(x) for x in data[idx + 1: idx + 1 + n]]
        idx += 1 + n
        best = p[:]
        for l in range(n):
            for r in range(l, n):
                q = p[:l] + p[l:r + 1][::-1] + p[r + 1:]
                if q < best:
                    best = q
        out.append(" ".join(map(str, best)))
    print("\n".join(out))


main()
