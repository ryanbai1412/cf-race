import math
import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        k = int(data[i])
        out.append(str(100 // math.gcd(k, 100)))
    sys.stdout.write("\n".join(out) + "\n")


main()
