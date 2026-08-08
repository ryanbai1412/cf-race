import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        p += 1  # n
        b = data[p].decode(); p += 1
        prev = -1
        a = []
        for ch in b:
            bi = ord(ch) - 48
            c = bi + 1
            if c == prev:
                c = bi
            a.append(str(c - bi))
            prev = c
        out.append("".join(a))
    sys.stdout.write("\n".join(out) + "\n")


main()
