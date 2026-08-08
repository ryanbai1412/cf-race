"""Independent brute force: try buying k matches, check a+b=c is assemblable."""
import sys


def ok(total):
    # need a,b,c > 0 with a+b=c and a+b+c = total => total = 2c, c >= 2
    return total % 2 == 0 and total >= 4


def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    out = []
    for i in range(1, q + 1):
        n = int(data[i])
        k = 0
        while not ok(n + k):
            k += 1
        out.append(str(k))
    print("\n".join(out))


main()
