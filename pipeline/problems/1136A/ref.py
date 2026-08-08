import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    rs = [int(data[2 + 2 * i]) for i in range(n)]
    k = int(data[1 + 2 * n])
    print(sum(1 for r in rs if r >= k))


main()
