import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = sum(int(x) for x in data[1 + 4 * i:5 + 4 * i])
        out.append("0" if s == 0 else ("2" if s == 4 else "1"))
    sys.stdout.write("\n".join(out) + "\n")


main()
