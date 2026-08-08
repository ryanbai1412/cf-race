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
        out.append(str(ord(max(s)) - ord("a") + 1))
    sys.stdout.write("\n".join(out) + "\n")


main()
