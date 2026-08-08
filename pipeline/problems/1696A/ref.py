import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); z = int(data[pos + 1]); pos += 2
        best = 0
        for x in data[pos:pos + n]:
            v = int(x) | z
            if v > best:
                best = v
        pos += n
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
