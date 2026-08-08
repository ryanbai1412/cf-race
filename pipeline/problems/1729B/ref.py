import sys


def decode(t: str) -> str:
    res = []
    i = len(t) - 1
    while i >= 0:
        if t[i] == "0":
            num = int(t[i - 2 : i])
            i -= 3
        else:
            num = int(t[i])
            i -= 1
        res.append(chr(ord("a") + num - 1))
    return "".join(reversed(res))


def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    out = []
    idx = 1
    for _ in range(q):
        idx += 1  # n, unused
        out.append(decode(data[idx]))
        idx += 1
    sys.stdout.write("\n".join(out) + "\n")


main()
