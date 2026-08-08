import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    q = int(data[p])
    p += 1
    out = []
    for _ in range(q):
        n = int(data[p])
        p += 1
        a = list(map(int, data[p:p + n]))
        p += n
        s = sum(a)
        out.append(-(-s // n))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
