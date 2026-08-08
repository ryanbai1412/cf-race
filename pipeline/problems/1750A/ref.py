import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = data[idx:idx + n]
        idx += n
        out.append("Yes" if a[0] == "1" else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
