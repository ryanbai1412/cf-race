import sys


def solve(a, b, x, y):
    best = 0
    for x1 in range(a):
        for x2 in range(x1, a):
            for y1 in range(b):
                for y2 in range(y1, b):
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        continue
                    best = max(best, (x2 - x1 + 1) * (y2 - y1 + 1))
    return best


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, x, y = (int(v) for v in data[1 + 4 * i:5 + 4 * i])
        out.append(solve(a, b, x, y))
    print("\n".join(map(str, out)))


main()
