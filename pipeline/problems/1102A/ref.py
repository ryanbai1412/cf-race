import sys


def main():
    n = int(sys.stdin.read().split()[0])
    print(n * (n + 1) // 2 % 2)


main()
