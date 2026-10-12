import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend (hexagon with sides a,b,c,a,b,c), input (2<=a,b,c<=1000), output present."


def solve(s):
    a, b, c = ints(s)
    return f"{a * b + b * c + c * a - a - b - c + 1}\n"


def cases(g):
    out = [("boundary", "all minimal", fmt([2, 2, 2])), ("boundary", "one side minimal", fmt([2, 1000, 1000])),
           ("adversarial", "two sides minimal", fmt([1000, 2, 2])), ("adversarial", "permuted sides", fmt([3, 2, 1000])),
           ("maxSize", "all maximal", fmt([1000, 1000, 1000])), ("maxSize", "near maximal", fmt([999, 1000, 998]))]
    out += fill(g, lambda g: fmt([g.randint(2, 1000) for _ in range(3)]), 70)
    out += fill(g, lambda g: fmt([g.randint(2, 10) for _ in range(3)]), 50, reason="small sides")
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
