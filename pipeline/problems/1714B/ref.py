import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos:pos + n]; pos += n
        seen = set()
        keep = 0
        for v in reversed(a):
            if v in seen:
                break
            seen.add(v)
            keep += 1
        out.append(str(n - keep))
    sys.stdout.write("\n".join(out) + "\n")


main()
