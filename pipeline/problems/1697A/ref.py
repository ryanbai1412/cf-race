import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        s = sum(int(x) for x in data[pos:pos + n]); pos += n
        out.append(max(0, s - m))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
