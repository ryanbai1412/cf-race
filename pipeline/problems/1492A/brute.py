"""Independent solution: for each swimmer, walk forward over multiples until
reaching or passing p, then take the minimum wait."""
import sys


def wait(p, x):
    m = 0
    while m < p:
        m += x
    return m - p


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        p, a, b, c = (int(x) for x in data[1 + 4 * i:5 + 4 * i])
        out.append(str(min(wait(p, a), wait(p, b), wait(p, c))))
    sys.stdout.write("\n".join(out) + "\n")


main()
