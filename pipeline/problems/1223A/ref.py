import sys


def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    out = []
    for i in range(1, q + 1):
        n = int(data[i])
        out.append("2" if n == 2 else str(n % 2))
    print("\n".join(out))


main()
