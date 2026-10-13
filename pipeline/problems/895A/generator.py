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
STATEMENT = "Legend (two continuous sectors, minimal difference), input (1<=n<=360, 1<=ai<=360, sum 360), output present."


def solve(s):
    a = ints(s)[1:]
    n, best = len(a), 360
    for i in range(n):
        t = 0
        for j in range(n):
            t += a[(i + j) % n]
            best = min(best, abs(360 - 2 * t))
    return f"{best}\n"


def split(g, parts):
    cuts = sorted(g.sample(range(1, 360), parts - 1))
    return [b - a for a, b in zip([0] + cuts, cuts + [360])]


def cases(g):
    out = [("boundary", "n=1", fmt(1, [360])), ("boundary", "n=2 halves", fmt(2, [180, 180])),
           ("adversarial", "one huge piece", fmt(2, [359, 1])), ("adversarial", "wraparound best", fmt(4, [170, 30, 150, 10])),
           ("maxSize", "n=360", fmt(360, [1] * 360))]
    out += fill(g, lambda g: fmt((p := g.randint(1, 8)), split(g, p)), 90, reason="small random")
    out += fill(g, lambda g: fmt((p := g.randint(9, 359)), split(g, p)), 25)
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
