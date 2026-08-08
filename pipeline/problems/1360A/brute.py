"""Independent brute force for 1360A: try every square side s and every pair of
integer placements/orientations of the two rectangles, checking they fit without
overlapping. Small a, b only. (Optimal placements can be taken integral since
all inputs are integers.)"""
import sys


def fits(a, b, s):
    for w1, h1 in {(a, b), (b, a)}:
        for w2, h2 in {(a, b), (b, a)}:
            if w1 > s or h1 > s or w2 > s or h2 > s:
                continue
            for x1 in range(s - w1 + 1):
                for y1 in range(s - h1 + 1):
                    for x2 in range(s - w2 + 1):
                        for y2 in range(s - h2 + 1):
                            ox = min(x1 + w1, x2 + w2) - max(x1, x2)
                            oy = min(y1 + h1, y2 + h2) - max(y1, y2)
                            if ox <= 0 or oy <= 0:
                                return True
    return False


def solve(a, b):
    s = max(a, b)
    while not fits(a, b, s):
        s += 1
    return s * s


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 2 * i]); b = int(data[2 + 2 * i])
        out.append(solve(a, b))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
