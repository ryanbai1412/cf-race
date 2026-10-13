import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Count then ascending values; unique, exact token comparison."
STATEMENT = "Legend (x + digitsum(x) = n), input (1<=n<=1e9), output present."


def solve(s):
    n = int(s)
    xs = [x for x in range(max(1, n - 90), n) if x + sum(map(int, str(x))) == n]
    return "\n".join(map(str, [len(xs)] + xs)) + "\n"


def cases(g):
    E = 10 ** 9
    out = [("boundary", "n=1", fmt(1)), ("boundary", "n=2", fmt(2)), ("boundary", "n=1e9", fmt(E)),
           ("adversarial", "two solutions n=1000000001-? candidate", fmt(101)), ("adversarial", "n=999999999", fmt(999999999)),
           ("maxSize", "n=1e9-1 region", fmt(E - 7))]
    out += [("random", "small n", fmt(n)) for n in range(3, 60)]
    out += fill(g, lambda g: fmt((x := g.randint(1, E - 100)) + sum(map(int, str(x)))), 40, reason="constructed solvable")
    out += fill(g, lambda g: fmt(g.randint(1, E)), 15)
    return [c for c in out if int(c[2]) <= E]


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
