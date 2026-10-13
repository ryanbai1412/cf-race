import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer string; unique, exact token comparison."
STATEMENT = "Legend (seven-segment digits, at most n segments, max number), input (2<=n<=1e5), output present."


def solve(s):
    n = int(s)
    return ("7" + "1" * ((n - 3) // 2) if n % 2 else "1" * (n // 2)) + "\n"


def cases(g):
    out = [("boundary", "n=2", fmt(2)), ("boundary", "n=3", fmt(3)), ("boundary", "n=1e5", fmt(10 ** 5)),
           ("adversarial", "n=5", fmt(5)), ("adversarial", "n=4", fmt(4)), ("maxSize", "n=99999", fmt(99999))]
    out += [("random", "small n", fmt(n)) for n in range(6, 60)]
    out += fill(g, lambda g: fmt(g.randint(60, 10 ** 5)), 50)
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
