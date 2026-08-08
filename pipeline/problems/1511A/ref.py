import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        r = data[pos : pos + n]
        pos += n
        out.append(sum(1 for x in r if x != "2"))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
