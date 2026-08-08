import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        xs = list(map(int, data[pos:pos + n])); pos += n
        bases = {xs[j] - xs[i] for i in range(n) for j in range(i + 1, n)}
        out.append(str(len(bases)))
    sys.stdout.write("\n".join(out) + "\n")


main()
