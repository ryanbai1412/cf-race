import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        pos += 1  # n
        s = data[pos]; pos += 1
        ok = any(s[:k] == "2020"[:k] and (s[len(s) - (4 - k):] if k < 4 else "") == "2020"[k:]
                 for k in range(5))
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
