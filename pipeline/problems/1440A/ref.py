import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); c0 = int(data[p + 1]); c1 = int(data[p + 2]); h = int(data[p + 3])
        p += 4
        s = data[p].decode(); p += 1
        total = 0
        for ch in s:
            if ch == "0":
                total += min(c0, c1 + h)
            else:
                total += min(c1, c0 + h)
        out.append(total)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
