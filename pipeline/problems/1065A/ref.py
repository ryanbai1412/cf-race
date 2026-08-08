import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s, a, b, c = (int(x) for x in data[1 + 4 * i:5 + 4 * i])
        k = s // c
        out.append(k + (k // a) * b)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
