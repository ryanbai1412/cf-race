import sys


def need(me, o1, o2):
    m = max(o1, o2)
    if me > m:
        return 0
    return m - me + 1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b, c = map(int, data[1 + 3 * i:4 + 3 * i])
        out.append(f"{need(a, b, c)} {need(b, a, c)} {need(c, a, b)}")
    sys.stdout.write("\n".join(out) + "\n")


main()
