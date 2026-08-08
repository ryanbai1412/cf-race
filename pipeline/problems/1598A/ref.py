import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        r1 = data[pos]; r2 = data[pos + 1]; pos += 2
        blocked = any(r1[i] == "1" and r2[i] == "1" for i in range(n))
        out.append("NO" if blocked else "YES")
    sys.stdout.write("\n".join(out) + "\n")


main()
