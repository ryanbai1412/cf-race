"""Independent solution: for each hero, simulate fighting the weakest other
hero repeatedly; a hero can win forever iff its level ever strictly exceeds
some other hero's level."""
import sys


def can_win(a, i):
    lvl = list(a)
    for _ in range(4 * len(a) + 10):
        others = [lvl[j] for j in range(len(lvl)) if j != i]
        m = min(others)
        if lvl[i] > m:
            return True
        return False
    return False


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = list(map(int, data[p:p + n])); p += n
        out.append(str(sum(1 for i in range(n) if can_win(a, i))))
    sys.stdout.write("\n".join(out) + "\n")


main()
