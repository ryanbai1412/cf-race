import sys
from itertools import combinations


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        s = data[idx]; idx += 1
        ok = False
        if n >= 11:
            for c in combinations(range(n), 11):
                if s[c[0]] == "8":
                    ok = True
                    break
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
