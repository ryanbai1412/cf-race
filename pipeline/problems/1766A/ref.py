import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        out.append(str(9 * (len(s) - 1) + int(s[0])))
    sys.stdout.write("\n".join(out) + "\n")


main()
