import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer or -1; unique, exact token comparison."
STATEMENT = "Legend (glass at i moves to p_i), input (1<=n<=1e5, 1<=s,t<=n, distinct p), output present."


def solve(s):
    v = ints(s)
    n, a, b = v[:3]
    p = v[3:]
    seen, cur, k = set(), a, 0
    while cur != b:
        if cur in seen:
            return "-1\n"
        seen.add(cur)
        cur = p[cur - 1]
        k += 1
    return f"{k}\n"


def make(g, n, cycle=False):
    p = list(range(1, n + 1))
    if cycle:
        order = p[:]
        g.shuffle(order)
        p = [0] * n
        for i in range(n):
            p[order[i] - 1] = order[(i + 1) % n]
    else:
        g.shuffle(p)
    return fmt([n, g.randint(1, n), g.randint(1, n)], p)


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=1", fmt([1, 1, 1], [1])), ("boundary", "s=t (0) with moves possible", fmt([3, 2, 2], [2, 3, 1])),
           ("adversarial", "fixed point s != t (-1)", fmt([3, 1, 2], [1, 3, 2])),
           ("maxSize", "n=1e5 single cycle, t just before s (n-1)", fmt([N, 1, N], list(range(2, N + 1)) + [1])),
           ("maxSize", "n=1e5 random single cycle", make(g, N, True)), ("maxSize", "n=1e5 identity, s!=t", fmt([N, 1, N], list(range(1, N + 1))))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.random() < 0.5), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), g.random() < 0.5), 30)
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
