"""Alternative implementation using per-person sets."""
import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        lists = []
        for _ in range(3):
            lists.append(data[idx:idx + n])
            idx += n
        sets = [set(l) for l in lists]
        scores = []
        for i in range(3):
            s = 0
            for w in lists[i]:
                writers = sum(1 for st in sets if w in st)
                s += 3 if writers == 1 else (1 if writers == 2 else 0)
            scores.append(s)
        out.append(" ".join(map(str, scores)))
    print("\n".join(out))


main()
