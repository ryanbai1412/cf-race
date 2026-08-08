import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        l, r, k = (int(x) for x in data[idx : idx + 3])
        idx += 3
        if l == r:
            out.append("YES" if l > 1 else "NO")
        else:
            odds = (r + 1) // 2 - l // 2
            out.append("YES" if k >= odds else "NO")
    print("\n".join(out))


main()
