import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, k1, k2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        w, b = int(data[idx + 3]), int(data[idx + 4])
        idx += 5
        white = k1 + k2
        black = 2 * n - white
        out.append("YES" if w <= white // 2 and b <= black // 2 else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
