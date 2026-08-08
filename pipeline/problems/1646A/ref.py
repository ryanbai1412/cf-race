import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i])
        s = int(data[2 + 2 * i])
        out.append(str(s // (n * n)))
    sys.stdout.write("\n".join(out) + "\n")


main()
