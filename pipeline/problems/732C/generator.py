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
STATEMENT = "Legend (arrival/departure any meal boundary, minimise missed meals), input (0<=b,d,s<=1e18, b+d+s>=1), output present."


def solve(s):
    v = ints(s)
    m = max(v)
    return f"{sum(max(0, m - 1 - x) for x in v)}\n"


def cases(g):
    E = 10 ** 18
    out = [("boundary", "1 0 0", fmt([1, 0, 0])), ("boundary", "0 0 1", fmt([0, 0, 1])), ("boundary", "all max", fmt([E, E, E])),
           ("adversarial", "max with zeros", fmt([E, 0, 0])), ("adversarial", "differ by one", fmt([E, E - 1, E - 1])), ("adversarial", "0 1 1", fmt([0, 1, 1])),
           ("maxSize", "max 0 max", fmt([E, 0, E]))]
    out += fill(g, lambda g: fmt([g.randint(0, 4) for _ in range(3)]), 60, reason="small random")
    out += fill(g, lambda g: fmt([g.randint(0, E) for _ in range(3)]), 30)
    out += fill(g, lambda g: fmt([(b := g.randint(1, E)) - g.randint(0, 2) for _ in range(3)]), 25, reason="near-equal large")
    return [c for c in out if sum(ints(c[2])) >= 1]


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
