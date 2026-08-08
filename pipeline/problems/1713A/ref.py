import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        xs, ys = [0], [0]
        for _ in range(n):
            x, y = int(data[pos]), int(data[pos + 1]); pos += 2
            xs.append(x)
            ys.append(y)
        ans = 2 * (max(xs) - min(xs) + max(ys) - min(ys))
        out.append(str(ans))
    print("\n".join(out))


main()
