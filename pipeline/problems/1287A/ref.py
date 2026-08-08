import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        idx += 1  # k
        s = data[idx]; idx += 1
        best = 0
        cur = -1
        for ch in s:
            if ch == "A":
                cur = 0
            elif cur >= 0:
                cur += 1
                best = max(best, cur)
        out.append(best)
    print("\n".join(map(str, out)))


main()
