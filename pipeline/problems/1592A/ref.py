import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); h = int(data[pos + 1]); pos += 2
        a = data[pos:pos + n]
        pos += n
        vals = sorted(map(int, a), reverse=True)
        x, y = vals[0], vals[1]
        s = x + y
        k = h // s
        rem = h - k * s
        if rem == 0:
            ans = 2 * k
        elif rem <= x:
            ans = 2 * k + 1
        else:
            ans = 2 * k + 2
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
