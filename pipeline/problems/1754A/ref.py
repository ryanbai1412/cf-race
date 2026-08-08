import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    i = 1
    for _ in range(t):
        i += 1  # n
        s = data[i]
        i += 1
        c = 0
        for ch in s:
            if ch == "Q":
                c += 1
            elif c > 0:
                c -= 1
        out.append("Yes" if c == 0 else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
