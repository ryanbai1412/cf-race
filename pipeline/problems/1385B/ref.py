import sys


def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(next(it)) for _ in range(2 * n)]
        seen = set()
        p = []
        for x in a:
            if x not in seen:
                seen.add(x)
                p.append(x)
        out.append(" ".join(map(str, p)))
    sys.stdout.write("\n".join(out) + "\n")


main()
