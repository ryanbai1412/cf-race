import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        ok = all(s.index(k) < s.index(k.upper()) for k in "rgb")
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
