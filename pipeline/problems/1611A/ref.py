import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        if int(s[-1]) % 2 == 0:
            out.append(0)
        elif int(s[0]) % 2 == 0:
            out.append(1)
        elif any(int(c) % 2 == 0 for c in s):
            out.append(2)
        else:
            out.append(-1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
