import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        b = data[i].decode()
        out.append(b[0] + b[1::2])
    sys.stdout.write("\n".join(out) + "\n")


main()
