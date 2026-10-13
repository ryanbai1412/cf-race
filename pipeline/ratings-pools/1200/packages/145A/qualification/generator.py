import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (flip or swap digits), input (two equal-length 4/7 strings, length<=1e5), output present."


def solve(s):
    a, b = s.split()
    x = sum(1 for p, q in zip(a, b) if p == "4" and q == "7")
    y = sum(1 for p, q in zip(a, b) if p == "7" and q == "4")
    return f"{max(x, y)}\n"


def word(g, n):
    return "".join(g.choice("47") for _ in range(n))


def cases(g):
    N = 10 ** 5
    out = [("boundary", "length 1 equal", fmt("4", "4")), ("boundary", "length 1 differ", fmt("4", "7")),
           ("adversarial", "only swaps needed", fmt("4747", "7474")), ("adversarial", "only flips needed", fmt("4444", "7777")),
           ("maxSize", "length 1e5 all different", fmt("4" * N, "7" * N)), ("maxSize", "length 1e5 random", fmt(word(g, N), word(g, N)))]
    out += fill(g, lambda g: (lambda n: fmt(word(g, n), word(g, n)))(g.randint(1, 10)), 80, reason="small random")
    out += fill(g, lambda g: (lambda n: fmt(word(g, n), word(g, n)))(g.randint(10, 3000)), 30)
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
