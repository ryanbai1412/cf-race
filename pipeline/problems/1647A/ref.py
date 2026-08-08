import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        k, r = divmod(n, 3)
        if r == 0:
            out.append("21" * k)
        elif r == 1:
            out.append("1" + "21" * k)
        else:
            out.append("21" * k + "2")
    print("\n".join(out))


main()
