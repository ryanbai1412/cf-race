import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        odd = sum(int(x) & 1 for x in data[pos:pos + n]); pos += n
        out.append(min(odd, n - odd))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
