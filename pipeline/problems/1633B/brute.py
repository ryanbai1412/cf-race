import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        best = 0
        for l in range(len(s)):
            for r in range(l + 1, len(s) + 1):
                sub = s[l:r]
                c0 = sub.count("0")
                c1 = len(sub) - c0
                if c0 != c1:
                    best = max(best, min(c0, c1))
        out.append(str(best))
    print("\n".join(out))


main()
