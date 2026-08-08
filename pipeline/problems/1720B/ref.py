import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = sorted(map(int, data[idx:idx + n])); idx += n
        out.append(a[-1] + a[-2] - a[0] - a[1])
    print("\n".join(map(str, out)))


main()
