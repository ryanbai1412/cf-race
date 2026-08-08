import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        l = int(data[1 + 2 * i])
        r = int(data[2 + 2 * i])
        out.append((r - 1) // 2 if 2 * l <= r else r - l)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
