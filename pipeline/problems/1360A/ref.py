import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 2 * i]); b = int(data[2 + 2 * i])
        lo, hi = min(a, b), max(a, b)
        s = max(hi, 2 * lo)
        out.append(s * s)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
