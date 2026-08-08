import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i]); m = int(data[2 + 2 * i])
        out.append((n * m + 1) // 2)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
