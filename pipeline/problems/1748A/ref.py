import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = [str((int(data[i]) + 1) // 2) for i in range(1, t + 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
