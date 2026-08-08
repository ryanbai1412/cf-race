import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1 : 1 + n]))
    print(sum(abs(x) for x in a))


main()
