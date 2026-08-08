import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        c1 = a.count(1)
        c2 = a.count(2)
        ok = c1 % 2 == 0 and (c2 % 2 == 0 or c1 >= 2)
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
