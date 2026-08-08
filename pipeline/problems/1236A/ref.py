import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c = map(int, data[1 + 3 * i:4 + 3 * i])
        # operation 2 consumes only one stone of b, so run it first
        k2 = min(b, c // 2)
        b -= k2
        k1 = min(a, b // 2)
        out.append(3 * (k1 + k2))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
