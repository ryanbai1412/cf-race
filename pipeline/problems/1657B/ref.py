import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n, B, x, y = (int(v) for v in data[pos:pos + 4])
        pos += 4
        cur = 0
        total = 0
        for _ in range(n):
            if cur + x <= B:
                cur += x
            else:
                cur -= y
            total += cur
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
