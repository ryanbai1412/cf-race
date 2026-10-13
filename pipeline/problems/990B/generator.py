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
STATEMENT = "Legend (i swallows j if aj < ai <= aj + K), input (1<=n<=2e5, 1<=K<=1e6, 1<=ai<=1e6), output present."
import bisect


def solve(s):
    v = ints(s)
    n, K = v[0], v[1]
    a = sorted(v[2:2 + n])
    left = 0
    for x in a:
        i = bisect.bisect_right(a, x)
        if not (i < n and a[i] <= x + K):
            left += 1
    return f"{left}\n"


def make(g, n, K, hi=10 ** 6):
    return fmt([n, K], [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N, E = 2 * 10 ** 5, 10 ** 6
    out = [("boundary", "n=1", fmt([1, 1], [E])), ("boundary", "K=1e6 all distinct", make(g, 10, E)),
           ("adversarial", "equal sizes cannot swallow", fmt([3, 5], [4, 4, 4])), ("adversarial", "chain step K", fmt([4, 1], [1, 2, 3, 4])),
           ("maxSize", "n=2e5 all equal", fmt([N, 1], [E] * N)), ("maxSize", "n=2e5 random K=1", make(g, N, 1)), ("maxSize", "n=2e5 random K=1e6", make(g, N, E))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(1, 3), 8), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), g.randint(1, 1000), g.choice([100, 5000, E])), 25)
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
