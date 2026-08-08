import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = data[idx:idx + 2 * n]
        idx += 2 * n
        odd = sum(1 for x in a if int(x) & 1)
        out.append("Yes" if odd == n else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
