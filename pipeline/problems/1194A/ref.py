import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i])
        x = int(data[2 + 2 * i])
        out.append(2 * x)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
