import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    i = 1
    for _ in range(t):
        a, b, c = int(data[i]), int(data[i + 1]), int(data[i + 2])
        i += 3
        out.append(str(sorted((a, b, c))[1]))
    sys.stdout.write("\n".join(out) + "\n")


main()
