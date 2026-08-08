import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c = map(int, data[1 + 3 * i:4 + 3 * i])
        out.append(0 if (a + b + c) % 3 == 0 else 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
