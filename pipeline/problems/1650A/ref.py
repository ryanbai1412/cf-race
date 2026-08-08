import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = data[1 + 2 * i]
        c = data[2 + 2 * i]
        out.append("YES" if any(s[j] == c for j in range(0, len(s), 2))
                   else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
