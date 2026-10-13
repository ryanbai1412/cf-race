import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer count of sessions; unique, exact token comparison."
STATEMENT = "Legend (each session raises one soldier of every distinct rank < k), input (1<=n,k<=100, non-decreasing 1<=ai<=k), output present."


def solve(s):
    v = ints(s)
    k, a = v[1], v[2:]
    sessions = 0
    while any(x < k for x in a):
        seen, nxt = set(), []
        for x in a:
            if x < k and x not in seen:
                seen.add(x)
                nxt.append(x + 1)
            else:
                nxt.append(x)
        a = sorted(nxt)
        sessions += 1
    return f"{sessions}\n"


def make(g, n, k):
    return fmt([n, k], sorted(g.randint(1, k) for _ in range(n)))


def cases(g):
    out = [("boundary", "n=k=1", fmt([1, 1], [1])), ("boundary", "all already max", fmt([3, 5], [5, 5, 5])),
           ("adversarial", "all equal rank 1", fmt([4, 3], [1, 1, 1, 1])),
           ("maxSize", "n=k=100 all 1 (max sessions)", fmt([100, 100], [1] * 100)), ("maxSize", "n=k=100 random", make(g, 100, 100)),
           ("maxSize", "n=100 k=1", fmt([100, 1], [1] * 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 6)), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100)), 30)
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
