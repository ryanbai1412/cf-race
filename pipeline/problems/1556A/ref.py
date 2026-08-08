import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        c = int(data[1 + 2 * i])
        d = int(data[2 + 2 * i])
        if (c + d) % 2 == 1:
            out.append(-1)
        elif c == d:
            out.append(0 if c == 0 else 1)
        else:
            out.append(2)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
