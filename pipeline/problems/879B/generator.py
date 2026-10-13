import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (winner stays, k wins in a row), input (2<=n<=500, 2<=k<=1e12, permutation), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    cur, wins = a[0], 0
    for x in a[1:]:
        if x > cur:
            cur, wins = x, 1
        else:
            wins += 1
        if wins >= k:
            break
    return f"{cur}\n"


def make(g, n, k):
    p = list(range(1, n + 1))
    g.shuffle(p)
    return fmt([n, k], p)


def cases(g):
    out = [("boundary", "n=2 k=2", fmt([2, 2], [1, 2])), ("boundary", "k=1e12", make(g, 500, 10 ** 12)),
           ("adversarial", "max first", fmt([4, 2], [4, 1, 2, 3])), ("adversarial", "increasing", fmt([5, 2], [1, 2, 3, 4, 5])),
           ("adversarial", "k exactly reached late", fmt([5, 2], [2, 1, 5, 3, 4])),
           ("maxSize", "n=500 k=499", make(g, 500, 499)), ("maxSize", "n=500 decreasing k=2", fmt([500, 2], list(range(500, 0, -1))))]
    out += fill(g, lambda g: make(g, g.randint(2, 7), g.randint(2, 8)), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(8, 500), g.choice([2, 3, g.randint(2, 600), 10 ** 12])), 25)
    return out


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
