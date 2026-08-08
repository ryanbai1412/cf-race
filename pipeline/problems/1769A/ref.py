import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    out = []
    prev = None
    for i in range(n):
        v = a[i] - (i + 1)
        if prev is not None:
            v = max(v, prev + 1)
        out.append(v)
        prev = v
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
