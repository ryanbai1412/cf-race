import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer or -1; unique, exact token comparison."
STATEMENT = "Legend (sets to exactly k points, maximise sets or -1), input (1<=k<=1e9, 0<=a,b<=1e9, a+b>0), output present."


def solve(s):
    k, a, b = ints(s)
    t = a // k + b // k
    if t == 0 or (a % k and b // k == 0) or (b % k and a // k == 0):
        return "-1\n"
    return f"{t}\n"


def cases(g):
    E = 10 ** 9
    out = [("boundary", "k=1", fmt([1, E, E])), ("boundary", "a=0 b=k", fmt([5, 0, 5])), ("boundary", "k=1e9 a=1e9 b=0", fmt([E, E, 0])),
           ("adversarial", "remainder without opponent set", fmt([11, 11, 5])), ("adversarial", "impossible remainder", fmt([11, 2, 3])), ("adversarial", "a=0 b remainder", fmt([3, 0, 7])),
           ("maxSize", "k=2 large", fmt([2, E, E - 1]))]
    out += fill(g, lambda g: fmt([g.randint(1, 5), g.randint(0, 12), g.randint(0, 12)]), 90, reason="small random")
    out += fill(g, lambda g: fmt([(k := g.randint(1, E)), g.randint(0, E), g.randint(0, E)]), 30)
    return [c for c in out if sum(ints(c[2])[1:]) > 0]


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
