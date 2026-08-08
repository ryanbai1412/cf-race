import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i].decode()
        n = len(s)
        lo, hi = 0, n - 1
        ok = True
        for c in range(n, 0, -1):
            ch = chr(96 + c)
            if s[lo] == ch:
                lo += 1
            elif s[hi] == ch:
                hi -= 1
            else:
                ok = False
                break
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
