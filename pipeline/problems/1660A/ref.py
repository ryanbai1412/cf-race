import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 2 * i])
        b = int(data[2 + 2 * i])
        out.append("1" if a == 0 else str(a + 2 * b + 1))
    sys.stdout.write("\n".join(out) + "\n")


main()
