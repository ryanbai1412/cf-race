import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        d = int(s[0])
        L = len(s)
        out.append((d - 1) * 10 + L * (L + 1) // 2)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
