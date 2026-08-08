import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, m = int(data[idx]), int(data[idx + 1]); idx += 2
        s = sum(int(data[idx + i]) for i in range(n)); idx += n
        out.append(min(s, m))
    print("\n".join(map(str, out)))


main()
