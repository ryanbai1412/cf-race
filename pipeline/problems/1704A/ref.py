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
        n, m = int(nxt()), int(nxt())
        a = nxt().decode()
        b = nxt().decode()
        # last m-1 chars must match; b[0] must appear in a[:n-m+1]
        ok = a[n - m + 1:] == b[1:] and b[0] in a[:n - m + 1]
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
