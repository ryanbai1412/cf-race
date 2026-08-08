import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 3 * i])
        b = int(data[2 + 3 * i])
        c = int(data[3 + 3 * i])
        h = abs(a - b)
        n = 2 * h
        if h == 0 or a > n or b > n or c > n:
            out.append(-1)
        else:
            out.append((c + h - 1) % n + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
