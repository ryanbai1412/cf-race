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
STATEMENT = "Legend, input (1<=n<=2e5, permutation), output present."


def solve(s):
    v = ints(s)
    pos = [0] * (v[0] + 1)
    for i, f in enumerate(v[1:], 1):
        pos[f] = i
    return f"{sum(abs(pos[i + 1] - pos[i]) for i in range(1, v[0]))}\n"


def perm(g, n):
    p = list(range(1, n + 1))
    g.shuffle(p)
    return fmt(n, p)


def cases(g):
    N = 200000
    alt = [x for i in range(N // 2) for x in (i + 1, N - i)]
    out = [("boundary", "n=1", fmt(1, [1])), ("boundary", "n=2 reversed", fmt(2, [2, 1])),
           ("adversarial", "identity permutation", fmt(6, [1, 2, 3, 4, 5, 6])),
           ("maxSize", "n=2e5 alternating ends (answer ~2e10)", fmt(N, alt)),
           ("maxSize", "n=2e5 random", perm(g, N)), ("maxSize", "n=2e5 reversed", fmt(N, list(range(N, 0, -1))))]
    out += fill(g, lambda g: perm(g, g.randint(1, 8)), 80, reason="small random")
    out += fill(g, lambda g: perm(g, g.randint(9, 3000)), 50)
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
