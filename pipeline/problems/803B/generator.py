import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "n integers; unique, exact token comparison."
STATEMENT = "Legend (distance to nearest zero), input (1<=n<=2e5, -1e9<=ai<=1e9, at least one zero), output present."


def solve(s):
    v = ints(s)
    a = v[1:]
    n, INF = len(a), 10 ** 9
    d, last = [INF] * n, -INF
    for i in range(n):
        if a[i] == 0:
            last = i
        d[i] = i - last
    last = 3 * INF
    for i in range(n - 1, -1, -1):
        if a[i] == 0:
            last = i
        d[i] = min(d[i], last - i)
    return " ".join(map(str, d)) + "\n"


def make(g, n, p=0.2, big=False):
    a = [0 if g.random() < p else g.randint(-10 ** 9, 10 ** 9) if big else g.randint(-3, 3) for _ in range(n)]
    a[g.randrange(n)] = 0
    return fmt(n, a)


def cases(g):
    N = 2 * 10 ** 5
    out = [("boundary", "n=1", fmt(1, [0])), ("boundary", "zero at end", fmt(3, [5, -5, 0])),
           ("adversarial", "zeros at both ends", fmt(5, [0, 10 ** 9, -10 ** 9, 1, 0])),
           ("maxSize", "n=2e5 single zero at start", fmt(N, [0] + [1] * (N - 1))), ("maxSize", "n=2e5 single zero middle", fmt(N, [7] * (N // 2) + [0] + [7] * (N // 2 - 1))),
           ("maxSize", "n=2e5 random", make(g, N, 0.001, True))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), g.random()), 110, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(11, 3000), g.random() / 10, True), 25)
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
