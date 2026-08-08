"""Independent brute force: enumerate the number of hamburgers sold."""
import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        b, p, f = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        h, c = int(data[idx + 3]), int(data[idx + 4])
        idx += 5
        best = 0
        for nh in range(min(b // 2, p) + 1):
            nc = min((b - 2 * nh) // 2, f)
            best = max(best, nh * h + nc * c)
        out.append(str(best))
    print("\n".join(out))


main()
