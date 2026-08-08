import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        keys = set()
        ok = True
        for c in s:
            if c.islower():
                keys.add(c)
            elif c.lower() not in keys:
                ok = False
                break
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
