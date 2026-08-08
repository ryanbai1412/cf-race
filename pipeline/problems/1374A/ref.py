import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        x = int(data[1 + 3 * i]); y = int(data[2 + 3 * i]); n = int(data[3 + 3 * i])
        out.append(n - (n - y) % x)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
