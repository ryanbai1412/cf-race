import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    pos = 1
    for _ in range(t):
        pos += 1  # n
        s = data[pos]; pos += 1
        seen = set()
        ok = True
        prev = None
        for c in s:
            if c != prev:
                if c in seen:
                    ok = False
                    break
                seen.add(c)
                prev = c
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
