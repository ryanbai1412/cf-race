import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        k = len(set(data[pos:pos + n])); pos += n
        out.append(k if (n - k) % 2 == 0 else k - 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
