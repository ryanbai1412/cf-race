import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        k = int(data[idx + 1])
        s = data[idx + 2]
        idx += 3
        cur = {s}
        for _ in range(min(k, 3)):
            nxt = set()
            for x in cur:
                nxt.add(x + x[::-1])
                nxt.add(x[::-1] + x)
            cur = nxt
        out.append(str(len(cur)))
    print("\n".join(out))


main()
