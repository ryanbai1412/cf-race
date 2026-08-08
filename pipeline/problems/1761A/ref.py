import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    i = 1
    for _ in range(t):
        n, a, b = int(data[i]), int(data[i + 1]), int(data[i + 2])
        i += 3
        ok = (a == n and b == n) or (a + b <= n - 2)
        out.append("Yes" if ok else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
