import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        m = data[i].decode()
        out.append(str(int(m) - 10 ** (len(m) - 1)))
    sys.stdout.write("\n".join(out) + "\n")


main()
