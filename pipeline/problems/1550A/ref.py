import sys
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = int(data[i])
        k = isqrt(s)
        if k * k < s:
            k += 1
        out.append(k)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
