import sys


def main():
    data = sys.stdin.read().split()
    w, h = int(data[0]), int(data[1])
    u1, d1 = int(data[2]), int(data[3])
    u2, d2 = int(data[4]), int(data[5])
    stones = {d1: u1}
    stones[d2] = stones.get(d2, 0) + u2
    while h > 0:
        w += h
        if h in stones:
            w = max(0, w - stones[h])
        h -= 1
    print(w)


main()
