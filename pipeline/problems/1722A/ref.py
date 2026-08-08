import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = data[2 + 2 * i]
        out.append("YES" if sorted(s) == sorted("Timur") else "NO")
    print("\n".join(out))


main()
