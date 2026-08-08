import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        l = sorted(int(x) for x in data[idx : idx + 3])
        idx += 3
        ok = (
            l[2] == l[0] + l[1]
            or (l[0] == l[1] and l[2] % 2 == 0)
            or (l[1] == l[2] and l[0] % 2 == 0)
        )
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
