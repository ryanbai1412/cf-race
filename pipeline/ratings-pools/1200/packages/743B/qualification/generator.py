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
STATEMENT = "Legend (recursive sequence, find k-th element), input (1<=n<=50, 1<=k<=2^n-1), output present."


def solve(s):
    n, k = ints(s)
    return f"{(k & -k).bit_length()}\n"


def cases(g):
    out = [("boundary", "n=1 k=1", fmt([1, 1])), ("boundary", "n=50 k=2^49 (middle)", fmt([50, 2 ** 49])), ("boundary", "n=50 k=max", fmt([50, 2 ** 50 - 1])),
           ("adversarial", "n=50 k=2^48", fmt([50, 2 ** 48])), ("adversarial", "n=50 k=3*2^48", fmt([50, 3 * 2 ** 48])),
           ("maxSize", "n=50 k=2^50-2", fmt([50, 2 ** 50 - 2]))]
    out += [("random", "n=4 every k", fmt([4, k])) for k in range(1, 16)]
    out += fill(g, lambda g: fmt([(n := g.randint(1, 50)), g.randint(1, 2 ** n - 1)]), 60)
    out += fill(g, lambda g: fmt([50, g.randint(1, 2 ** 20) << g.randint(0, 29)]), 30, reason="power-of-two-heavy")
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
