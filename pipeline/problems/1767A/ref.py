import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        xs = []
        ys = []
        for _ in range(3):
            xs.append(int(data[pos]))
            ys.append(int(data[pos + 1]))
            pos += 2
        ok = len(set(xs)) == 3 or len(set(ys)) == 3
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
