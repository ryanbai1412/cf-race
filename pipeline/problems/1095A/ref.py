import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    out = []
    i = 0
    k = 1
    while i < n:
        out.append(t[i])
        i += k
        k += 1
    print("".join(out))


main()
