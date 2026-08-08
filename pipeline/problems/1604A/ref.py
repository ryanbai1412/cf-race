import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        ans = 0
        for i, x in enumerate(a, 1):
            ans = max(ans, x - i)
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
