import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = sorted(map(int, data[1 + 4 * i:5 + 4 * i]))
        out.append(str(a[0] * a[2]))
    sys.stdout.write("\n".join(out) + "\n")


main()
