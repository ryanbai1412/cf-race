import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Conan/Agasa; unique, exact token comparison."
STATEMENT = "Legend (remove card and all strictly smaller), input (1<=n<=1e5, 1<=ai<=1e5), output present."


def solve(s):
    a = ints(s)[1:]
    c = {}
    for x in a:
        c[x] = c.get(x, 0) + 1
    return "Conan\n" if any(v % 2 for v in c.values()) else "Agasa\n"


def make(g, n, hi, even=False):
    if even:
        a = [g.randint(1, hi) for _ in range(n // 2)] * 2
        g.shuffle(a)
        return fmt(len(a), a)
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=1", fmt(1, [N])), ("boundary", "pair", fmt(2, [7, 7])),
           ("adversarial", "all even counts", fmt(4, [1, 1, 2, 2])), ("adversarial", "odd smaller only", fmt(3, [1, 2, 2])),
           ("maxSize", "n=1e5 all equal", fmt(N, [N] * N)), ("maxSize", "n=1e5 paired", make(g, N, N, True)), ("maxSize", "n=1e5 random", make(g, N, N))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), 4, g.random() < 0.5), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 5000), g.choice([5, 1000, N]), g.random() < 0.6), 25)
    return [c for c in out if ints(c[2])[0] >= 1]


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
