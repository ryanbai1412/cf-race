import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        a, b, c = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        idx += 3
        out.append("YES" if (a + b == c or a + c == b or b + c == a) else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
