import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend, input (2<=n<=100, 1<=ai<=1000), output present."


def solve(s):
    v = ints(s)[1:]
    me, rest = v[0], v[1:]
    k = 0
    while me <= max(rest):
        i = rest.index(max(rest))
        rest[i] -= 1
        me += 1
        k += 1
    return f"{k}\n"


def cases(g):
    out = [("boundary", "n=2 already winning", fmt(2, [2, 1])), ("boundary", "n=2 tie", fmt(2, [1, 1])),
           ("adversarial", "Limak minimal, all others equal maximal", fmt(100, [1] + [1000] * 99)),
           ("adversarial", "one huge opponent", fmt(3, [1, 1000, 1])),
           ("maxSize", "n=100 all 1000", fmt(100, [1000] * 100)), ("maxSize", "n=100 random", fmt(100, [g.randint(1, 1000) for _ in range(100)]))]
    out += fill(g, lambda g: (lambda n: fmt(n, [g.randint(1, 1000) for _ in range(n)]))(g.randint(2, 100)), 60)
    out += fill(g, lambda g: (lambda n: fmt(n, [g.randint(1, 10) for _ in range(n)]))(g.randint(2, 8)), 60, reason="small")
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
