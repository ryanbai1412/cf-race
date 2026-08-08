import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        a, b, c, x, y = (int(v) for v in data[idx : idx + 5])
        idx += 5
        need = max(0, x - a) + max(0, y - b)
        out.append("YES" if need <= c else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
