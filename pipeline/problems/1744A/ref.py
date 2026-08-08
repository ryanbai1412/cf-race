import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = data[idx:idx + n]
        idx += n
        s = data[idx]
        idx += 1
        mp = {}
        ok = True
        for x, ch in zip(a, s):
            if mp.setdefault(x, ch) != ch:
                ok = False
                break
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
