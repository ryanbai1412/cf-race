import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        if k == 1:
            out.append((n - 1) // 2)
        else:
            out.append(sum(a[i] > a[i - 1] + a[i + 1] for i in range(1, n - 1)))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
