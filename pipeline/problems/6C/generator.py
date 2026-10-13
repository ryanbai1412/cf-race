import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Two integers; tie goes to Alice per statement, so unique; exact token comparison."
STATEMENT = "Legend (Alice from left, Bob from right, simultaneous start yields to Alice), input (1<=n<=1e5, 1<=ti<=1000), output present."


def solve(s):
    v = ints(s)
    t = v[1:]
    i, j, ta, tb = 0, len(t) - 1, 0, 0
    while i <= j:
        if ta <= tb:
            ta += t[i]
            i += 1
        else:
            tb += t[j]
            j -= 1
    return f"{i} {len(t) - i}\n"


def make(g, n, hi=1000):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=1 (Alice)", fmt(1, [1])), ("boundary", "n=2", fmt(2, [1000, 1])),
           ("adversarial", "simultaneous arrival at middle bar", fmt(3, [2, 5, 2])), ("adversarial", "all equal odd", fmt(5, [3] * 5)),
           ("maxSize", "n=1e5 all 1000", fmt(N, [1000] * N)), ("maxSize", "n=1e5 random", make(g, N)), ("maxSize", "n=1e5 all 1", fmt(N, [1] * N))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 5000)), 30)
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
