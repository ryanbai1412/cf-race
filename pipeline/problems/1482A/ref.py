import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 2 * i]); b = int(data[2 + 2 * i])
        out.append(str(a * b))
    sys.stdout.write("\n".join(out) + "\n")


main()
