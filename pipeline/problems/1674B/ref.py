import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        f = ord(s[0]) - 97
        g = ord(s[1]) - 97
        out.append(f * 25 + (g if g < f else g - 1) + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
