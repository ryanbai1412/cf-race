import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        px = int(data[p]); py = int(data[p + 1]); p += 2
        s = data[p]; p += 1
        r = s.count(b"R")
        l = s.count(b"L")
        u = s.count(b"U")
        d = s.count(b"D")
        ok = (px <= r if px >= 0 else -px <= l) and (py <= u if py >= 0 else -py <= d)
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
