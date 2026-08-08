import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1 + n
        k = 10 - n
        out.append(str(3 * k * (k - 1)))
    sys.stdout.write("\n".join(out) + "\n")


main()
