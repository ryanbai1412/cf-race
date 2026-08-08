import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = [str((int(data[i + 1]) + 1) // 10) for i in range(t)]
    sys.stdout.write("\n".join(out) + "\n")


main()
