import sys


def key(s: str) -> int:
    if s == "M":
        return 0
    return len(s) if s[-1] == "L" else -len(s)


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a, b = data[1 + 2 * i], data[2 + 2 * i]
        ka, kb = key(a), key(b)
        out.append("<" if ka < kb else ">" if ka > kb else "=")
    sys.stdout.write("\n".join(out) + "\n")


main()
