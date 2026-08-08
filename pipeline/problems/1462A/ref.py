import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        b = data[pos:pos + n]; pos += n
        res = []
        i, j = 0, n - 1
        while i < j:
            res.append(b[i])
            res.append(b[j])
            i += 1
            j -= 1
        if i == j:
            res.append(b[i])
        out.append(b" ".join(res))
    sys.stdout.buffer.write(b"\n".join(out) + b"\n")


main()
