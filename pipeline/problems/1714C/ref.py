import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = int(data[i])
        digits = []
        for d in range(9, 0, -1):
            if s >= d:
                digits.append(d)
                s -= d
        # s is now 0 because 9+8+...+1 = 45 >= any input
        out.append("".join(map(str, sorted(digits))))
    print("\n".join(out))


main()
