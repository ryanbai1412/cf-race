import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        r = int(data[i])
        if r >= 1900:
            d = 1
        elif r >= 1600:
            d = 2
        elif r >= 1400:
            d = 3
        else:
            d = 4
        out.append(f"Division {d}")
    sys.stdout.write("\n".join(out) + "\n")


main()
