import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        moves = 0
        while a % b != 0:
            a += 1
            moves += 1
        out.append(moves)
    print("\n".join(map(str, out)))


main()
