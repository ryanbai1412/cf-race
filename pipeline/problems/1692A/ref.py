import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c, d = (int(x) for x in data[1 + 4 * i:5 + 4 * i])
        out.append((b > a) + (c > a) + (d > a))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
