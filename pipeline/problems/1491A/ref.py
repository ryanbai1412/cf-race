import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    a = list(map(int, data[2:2 + n]))
    ones = sum(a)
    p = 2 + n
    out = []
    for _ in range(q):
        typ = data[p]; v = int(data[p + 1]); p += 2
        if typ == b"1":
            if a[v - 1]:
                a[v - 1] = 0
                ones -= 1
            else:
                a[v - 1] = 1
                ones += 1
        else:
            out.append("1" if v <= ones else "0")
    sys.stdout.write("\n".join(out) + "\n")


main()
