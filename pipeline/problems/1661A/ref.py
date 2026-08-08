import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        b = [int(x) for x in data[pos:pos + n]]; pos += n
        s = 0
        for i in range(n - 1):
            keep = abs(a[i] - a[i + 1]) + abs(b[i] - b[i + 1])
            swap = abs(a[i] - b[i + 1]) + abs(b[i] - a[i + 1])
            s += min(keep, swap)
        out.append(str(s))
    sys.stdout.write("\n".join(out) + "\n")


main()
