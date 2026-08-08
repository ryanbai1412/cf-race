import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    squares = {i * i for i in range(150)}
    out = []
    for i in range(t):
        x = int(data[1 + 2 * i])
        y = int(data[2 + 2 * i])
        d = x * x + y * y
        out.append("0" if d == 0 else "1" if d in squares else "2")
    sys.stdout.write("\n".join(out) + "\n")


main()
