import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        p = list(range(1, n + 1))
        # swap adjacent pairs from the top: (n-1,n), (n-3,n-2), ...
        j = n - 1
        while j >= 1:
            p[j], p[j - 1] = p[j - 1], p[j]
            j -= 2
        out.append(" ".join(map(str, p)))
    sys.stdout.write("\n".join(out) + "\n")


main()
