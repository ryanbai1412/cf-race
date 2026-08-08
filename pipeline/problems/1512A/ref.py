import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos : pos + n]
        pos += n
        majority = a[0] if a[0] in (a[1], a[2]) else a[1]
        for i, x in enumerate(a, 1):
            if x != majority:
                out.append(i)
                break
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
