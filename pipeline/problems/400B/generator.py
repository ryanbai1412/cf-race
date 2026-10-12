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
STATEMENT = "Legend (all chosen dwarves move until one hits candy or wall), input (1<=n<=1000, 2<=m<=1000, one G and one S per row), output present."


def solve(s):
    rows = s.split()[2:]
    d = set()
    for r in rows:
        gi, si = r.index("G"), r.index("S")
        if si < gi:
            return "-1\n"
        d.add(si - gi)
    return f"{len(d)}\n"


def row(g, m, forward=True):
    a, b = g.sample(range(m), 2)
    if forward and a > b:
        a, b = b, a
    r = ["*"] * m
    r[a], r[b] = "G", "S"
    return "".join(r)


def make(g, n, m, p_back=0.0):
    return fmt([n, m], *[row(g, m, g.random() >= p_back) for _ in range(n)])


def cases(g):
    out = [("boundary", "1x2 GS", fmt([1, 2], "GS")), ("boundary", "1x2 SG (-1)", fmt([1, 2], "SG")),
           ("adversarial", "all rows same distance", fmt([3, 5], "G***S", "G***S", "G***S")),
           ("adversarial", "one backwards row among many", fmt([3, 4], "G**S", "*GS*", "*S*G")),
           ("maxSize", "1000x1000 all forward", make(g, 1000, 1000)),
           ("maxSize", "1000x1000 G at 0 S at end", fmt([1000, 1000], *["G" + "*" * 998 + "S"] * 1000))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(2, 8), g.choice([0, 0, 0.1])), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(2, 100), g.choice([0, 0.01])), 25, reason="medium random")
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
