import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(v) for v in data[pos:pos + n]]; pos += n
        if n == 1:
            out.append("YES" if a[0] == 1 else "NO")
            continue
        a.sort()
        out.append("YES" if a[-1] - a[-2] <= 1 else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
