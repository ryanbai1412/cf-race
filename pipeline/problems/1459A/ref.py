import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        pos += 1  # n
        r = data[pos]; pos += 1
        b = data[pos]; pos += 1
        red = sum(1 for x, y in zip(r, b) if x > y)
        blue = sum(1 for x, y in zip(r, b) if x < y)
        out.append("RED" if red > blue else "BLUE" if blue > red else "EQUAL")
    sys.stdout.write("\n".join(out) + "\n")


main()
