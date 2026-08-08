import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        p, a, b, c = (int(x) for x in data[1 + 4 * i:5 + 4 * i])
        out.append(str(min(-p % a, -p % b, -p % c)))
    sys.stdout.write("\n".join(out) + "\n")


main()
