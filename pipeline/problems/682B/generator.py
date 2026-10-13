import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single maximum mex; unique, exact token comparison."
STATEMENT = "Legend (decrease elements to maximize mex), input (1<=n<=1e5, 1<=ai<=1e9), output present."


def solve(s):
    v = ints(s)
    mex = 1
    for a in sorted(v[1:]):
        if a >= mex:
            mex += 1
    return f"{mex}\n"


def make(g, n, hi=10 ** 9):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=1 a=1", fmt(1, [1])), ("boundary", "n=1 a=1e9", fmt(1, [10 ** 9])),
           ("adversarial", "all ones", fmt(4, [1, 1, 1, 1])),
           ("maxSize", "n=1e5 all 1e9 (mex n+1)", fmt(N, [10 ** 9] * N)), ("maxSize", "n=1e5 1..n shuffled", fmt(N, g.sample(range(1, N + 1), N))),
           ("maxSize", "n=1e5 random small values", make(g, N, 1000))]
    out += fill(g, lambda g: make(g, g.randint(1, 7), 6), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(8, 3000), g.choice([50, 3000, 10 ** 9])), 30)
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
