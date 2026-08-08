import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        b = s.count("B")
        out.append("YES" if 2 * b == len(s) else "NO")
    print("\n".join(out))


main()
