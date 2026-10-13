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
STATEMENT = "Legend (split into prefix/suffix, maximise sum of scores mod p; examples confirm cover), input (2<=N<=1e5, 2<=p<=1e4, 1<=ai<=1e6), output present."


def solve(s):
    v = ints(s)
    n, p = v[0], v[1]
    a = v[2:2 + n]
    tot, pre, best = sum(a), 0, 0
    for x in a[:-1]:
        pre += x
        best = max(best, pre % p + (tot - pre) % p)
    return f"{best}\n"


def make(g, n, p, hi=10 ** 6):
    return fmt([n, p], [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=2 p=2", fmt([2, 2], [1, 1])), ("boundary", "p=1e4 n=2", fmt([2, 10 ** 4], [10 ** 6, 10 ** 6])),
           ("adversarial", "sample 2", fmt([10, 12], [16, 3, 24, 13, 9, 8, 7, 5, 12, 12])),
           ("maxSize", "n=1e5 max values", fmt([N, 9973], [10 ** 6] * N)), ("maxSize", "n=1e5 random", make(g, N, 10 ** 4))]
    out += fill(g, lambda g: make(g, g.randint(2, 8), g.randint(2, 12), 30), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), g.randint(2, 10 ** 4)), 25)
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
