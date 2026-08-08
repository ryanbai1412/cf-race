import math
import sys


def ok(x):
    return math.gcd(x, sum(map(int, str(x)))) > 1


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        while not ok(n):
            n += 1
        out.append(n)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
