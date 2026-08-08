import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        out.append(str(n // 2 + 1))
    sys.stdout.write("\n".join(out) + "\n")


main()
