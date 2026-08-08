import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        if n % 2050:
            out.append("-1")
        else:
            out.append(str(sum(int(c) for c in str(n // 2050))))
    sys.stdout.write("\n".join(out) + "\n")


main()
