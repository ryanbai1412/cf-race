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
STATEMENT = "Legend (split into k segments, max of mins), input (1<=k<=n<=1e5, -1e9<=ai<=1e9), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a = v[2:2 + n]
    if k == 1:
        r = min(a)
    elif k == 2:
        r = max(a[0], a[-1])
    else:
        r = max(a)
    return f"{r}\n"


def make(g, n, k, lo=-10 ** 9, hi=10 ** 9):
    return fmt([n, k], [g.randint(lo, hi) for _ in range(n)])


def cases(g):
    N, E = 10 ** 5, 10 ** 9
    out = [("boundary", "n=k=1", fmt([1, 1], [-E])), ("boundary", "k=n", make(g, 5, 5)),
           ("adversarial", "k=2 max in middle", fmt([5, 2], [1, 9, 9, 9, 2])), ("adversarial", "k=2 ends", fmt([3, 2], [-E, 0, E])),
           ("maxSize", "n=1e5 k=1", make(g, N, 1)), ("maxSize", "n=1e5 k=2", make(g, N, 2)), ("maxSize", "n=1e5 k=3", make(g, N, 3))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 7)), g.randint(1, n), -5, 5), 90, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(8, 3000)), g.choice([1, 2, 3, g.randint(1, n)])), 25)
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
