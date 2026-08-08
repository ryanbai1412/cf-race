import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0

    def nxt():
        nonlocal pos
        v = data[pos]
        pos += 1
        return v

    t = int(nxt())
    out = []
    for _ in range(t):
        n = int(nxt())
        a = [int(nxt()) for _ in range(n)]
        res = []
        for i in range(n):
            b = int(nxt())
            moves = nxt().decode()
            d = a[i]
            for ch in moves:
                d = (d - 1) % 10 if ch == "U" else (d + 1) % 10
            res.append(str(d))
        out.append(" ".join(res))
    sys.stdout.write("\n".join(out) + "\n")


main()
