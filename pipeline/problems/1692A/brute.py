"""Independent alternative: sort-based rank computation."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        vals = [int(x) for x in data[1 + 4 * i:5 + 4 * i]]
        a = vals[0]
        order = sorted(vals, reverse=True)
        out.append(order.index(a))  # distinct values, so index = #ahead
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
