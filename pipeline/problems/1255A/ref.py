import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        d = abs(a - b)
        out.append(d // 5 + d % 5 // 2 + d % 5 % 2)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
