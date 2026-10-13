import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer (0 or 1); unique, exact token comparison."
STATEMENT = "Legend (same company free, else |i-j|), input (1<=n<=1e5, 1<=a,b<=n, binary string length n), output present."


def solve(s):
    t = s.split()
    a, b, c = int(t[1]), int(t[2]), t[3]
    return "0\n" if c[a - 1] == c[b - 1] else "1\n"


def make(g, n):
    return fmt([n, g.randint(1, n), g.randint(1, n)], "".join(g.choice("01") for _ in range(n)))


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=1", fmt([1, 1, 1], "0")), ("boundary", "a=b", fmt([3, 2, 2], "101")),
           ("adversarial", "far endpoints differ", fmt([N, 1, N], "0" + "1" * (N - 1))), ("adversarial", "alternating", fmt([6, 1, 6], "010101")),
           ("maxSize", "n=1e5 random", make(g, N)), ("maxSize", "n=1e5 same company", fmt([N, 1, N], "1" * N))]
    out += fill(g, lambda g: make(g, g.randint(1, 8)), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 5000)), 25)
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
