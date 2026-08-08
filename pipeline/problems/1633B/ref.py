import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        c0 = s.count("0")
        c1 = len(s) - c0
        out.append(str(min(c0, c1) if c0 != c1 else c0 - 1))
    print("\n".join(out))


main()
