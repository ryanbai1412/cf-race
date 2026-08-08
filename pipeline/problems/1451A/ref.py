import sys


def moves(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    if n == 3:
        return 2
    if n % 2 == 0:
        return 2
    return 3


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = [moves(int(data[1 + i])) for i in range(t)]
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
