import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        k, r = divmod(n, 3)
        if r == 0:
            c1, c2 = k, k
        elif r == 1:
            c1, c2 = k + 1, k
        else:
            c1, c2 = k, k + 1
        out.append(f"{c1} {c2}")
    sys.stdout.write("\n".join(out) + "\n")


main()
