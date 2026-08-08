import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        s = data[idx + 1]
        idx += 2
        ok = n == 1 or (n == 2 and s[0] != s[1])
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
