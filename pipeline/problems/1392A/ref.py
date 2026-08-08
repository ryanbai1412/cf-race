import sys


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [next(it) for _ in range(n)]
        out.append(str(n if len(set(a)) == 1 else 1))
    sys.stdout.write("\n".join(out) + "\n")


main()
