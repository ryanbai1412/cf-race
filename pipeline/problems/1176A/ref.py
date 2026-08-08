import sys


def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    out = []
    for i in range(1, q + 1):
        n = int(data[i])
        moves = 0
        for p, cost in ((2, 1), (3, 2), (5, 3)):
            while n % p == 0:
                n //= p
                moves += cost
        out.append(moves if n == 1 else -1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
