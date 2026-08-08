import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n, m = int(data[2 * i - 1]), int(data[2 * i])
        # go right along row 1 (1..m), then down column m
        # cost = m(m+1)/2 + sum_{i=2..n} i*m
        out.append(str(m * (m + 1) // 2 + m * (n * (n + 1) // 2 - 1)))
    sys.stdout.write("\n".join(out) + "\n")


main()
