import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer or -1; unique, exact token comparison."
STATEMENT = "Legend, input (1<=n<=100, 1<=xi,yi<=6), output present."


def solve(s):
    v = ints(s)[1:]
    x, y = v[0::2], v[1::2]
    sx, sy = sum(x) % 2, sum(y) % 2
    if sx == 0 and sy == 0:
        return "0\n"
    if sx == 1 and sy == 1 and any((a + b) % 2 for a, b in zip(x, y)):
        return "1\n"
    return "-1\n"


def dom(g, n):
    return fmt(n, *[[g.randint(1, 6), g.randint(1, 6)] for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1 both even", fmt(1, [2, 4])), ("boundary", "n=1 mixed parity (-1)", fmt(1, [2, 3])),
           ("boundary", "n=1 both odd (-1)", fmt(1, [1, 3])),
           ("adversarial", "both sums odd, no mixed domino (-1)", fmt(2, [1, 1], [2, 2])),
           ("adversarial", "both sums odd, one mixed domino (1)", fmt(2, [1, 2], [2, 3])),
           ("maxSize", "n=100 all 6 6", fmt(100, *[[6, 6]] * 100)), ("maxSize", "n=100 random", dom(g, 100))]
    out += fill(g, lambda g: dom(g, g.randint(1, 100)), 60)
    out += fill(g, lambda g: dom(g, g.randint(1, 4)), 60, reason="tiny")
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
