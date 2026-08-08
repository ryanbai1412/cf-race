import sys

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n, m, r, c = map(int, data[1 + 4 * i:5 + 4 * i])
        out.append(str(max(r - 1, n - r) + max(c - 1, m - c)))
    sys.stdout.write("\n".join(out) + "\n")

main()
