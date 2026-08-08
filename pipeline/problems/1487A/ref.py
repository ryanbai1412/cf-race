import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = list(map(int, data[p:p + n])); p += n
        m = min(a)
        out.append(str(sum(1 for v in a if v > m)))
    sys.stdout.write("\n".join(out) + "\n")


main()
