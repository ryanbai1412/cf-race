import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        a = list(map(int, data[pos:pos + n])); pos += n
        b = list(map(int, data[pos:pos + n])); pos += n
        a.sort()
        b.sort(reverse=True)
        for i in range(k):
            if b[i] > a[i]:
                a[i] = b[i]
            else:
                break
        out.append(sum(a))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
