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
        for i in range(n):
            if p[i] != i + 1:
                j = p.index(i + 1, i + 1)
                p[i:j + 1] = p[i:j + 1][::-1]
                break
        out.append(" ".join(map(str, p)))
    print("\n".join(out))


main()
