import sys


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        if k % 2 == 1:
            d = max(a)
            res = [d - x for x in a]
        else:
            d = min(a)
            res = [x - d for x in a]
        out.append(" ".join(map(str, res)))
    sys.stdout.write("\n".join(out) + "\n")


main()
