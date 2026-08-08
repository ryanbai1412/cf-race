import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        xs = list(map(int, data[pos:pos + n])); pos += n
        used = -1
        cnt = 0
        for x in xs:
            if x > used:
                used = x
                cnt += 1
            elif x + 1 > used:
                used = x + 1
                cnt += 1
        out.append(str(cnt))
    sys.stdout.write("\n".join(out) + "\n")


main()
