"""Independent brute force: try every stick and every split point."""
import sys


def can(ls):
    for i in range(3):
        for a in range(1, ls[i]):
            b = ls[i] - a
            four = sorted(ls[:i] + ls[i + 1 :] + [a, b])
            if four[0] == four[1] and four[2] == four[3]:
                return True
    return False


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        ls = [int(x) for x in data[idx : idx + 3]]
        idx += 3
        print("YES" if can(ls) else "NO")


main()
