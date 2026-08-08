import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx]); m = int(data[idx + 1]); idx += 2
        if n == 1 and m == 1:
            out.append(0)
        else:
            out.append((n - 1) + (m - 1) + min(n, m))
    print("\n".join(map(str, out)))


main()
