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
STATEMENT = "Legend (plates from one cake each, maximise min pieces), input (1<=a,b<=100, 2<=n<=a+b), output present."


def solve(s):
    n, a, b = ints(s)
    return f"{max(min(a // i, b // (n - i)) for i in range(1, n) if i <= a and n - i <= b)}\n"


def make(g, hi):
    a, b = g.randint(1, hi), g.randint(1, hi)
    return fmt([g.randint(2, a + b), a, b])


def cases(g):
    out = [("boundary", "n=2 a=b=1", fmt([2, 1, 1])), ("boundary", "n=a+b max", fmt([200, 100, 100])), ("boundary", "n=2 max", fmt([2, 100, 100])),
           ("adversarial", "unbalanced", fmt([3, 1, 100])), ("adversarial", "sample", fmt([5, 2, 3])), ("maxSize", "n=199", fmt([199, 100, 100]))]
    out += fill(g, lambda g: make(g, 8), 70, reason="small random")
    out += fill(g, lambda g: make(g, 100), 50)
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
