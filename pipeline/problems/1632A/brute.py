import sys
from itertools import permutations


def has_pal(s):
    return any(s[i] == s[i + 1] for i in range(len(s) - 1)) or \
        any(s[i] == s[i + 2] for i in range(len(s) - 2))


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        s = data[idx + 1]
        idx += 2
        ok = any(not has_pal("".join(p)) for p in set(permutations(s)))
        out.append("YES" if ok else "NO")
    print("\n".join(out))


main()
