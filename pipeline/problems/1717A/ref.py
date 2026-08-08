import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        # a = g*x, b = g*y with gcd(x,y)=1 and x*y <= 3:
        # (1,1): n pairs; (1,2)/(2,1): 2*floor(n/2); (1,3)/(3,1): 2*floor(n/3)
        out.append(n + 2 * (n // 2) + 2 * (n // 3))
    print("\n".join(map(str, out)))


main()
