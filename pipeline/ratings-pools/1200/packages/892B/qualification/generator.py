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
STATEMENT = "Legend (i kills j in [i-Li, i)), input (1<=n<=1e6, 0<=Li<=1e9), output present."


def solve(s):
    v = ints(s)
    L = v[1:]
    alive, reach = 0, len(L)
    for i in range(len(L) - 1, -1, -1):
        if i < reach:
            alive += 1
        reach = min(reach, i - L[i])
    return f"{alive}\n"


def make(g, n, hi):
    return fmt(n, [g.randint(0, hi) for _ in range(n)])


def cases(g):
    N = 10 ** 6
    out = [("boundary", "n=1", fmt(1, [10 ** 9])), ("boundary", "n=2 kill", fmt(2, [0, 1])),
           ("adversarial", "huge claw at end", fmt(4, [0, 1, 0, 10])), ("adversarial", "all zero", fmt(5, [0] * 5)),
           ("maxSize", "n=1e6 zeros", fmt(N, [0] * N)), ("maxSize", "n=1e6 random small", make(g, N, 3))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), 4), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), g.choice([1, 5, 10 ** 9])), 25)
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
