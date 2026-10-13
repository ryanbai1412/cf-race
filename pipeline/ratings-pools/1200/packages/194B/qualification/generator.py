import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]


from math import gcd

CHECKER = "One integer per test case; unique, exact token comparison."
STATEMENT = "Legend (crosses every n+1 metres on 4n perimeter), input (1<=t<=1e4, 1<=ni<=1e9), output present."


def solve(s):
    v = ints(s)
    return "".join(f"{4 * n // gcd(4 * n, n + 1) + 1}\n" for n in v[1:])


def make(g, t, hi):
    return fmt(t, [g.randint(1, hi) for _ in range(t)])


def cases(g):
    out = [("boundary", "t=1 n=1", fmt(1, [1])), ("adversarial", "n+1 shares factors 2/4 with 4n", fmt(4, [3, 7, 11, 15])),
           ("maxSize", "t=1e4 all 1e9", fmt(10000, [10 ** 9] * 10000)), ("maxSize", "t=1e4 random", make(g, 10000, 10 ** 9)),
           ("boundary", "n=1e9-1 (n+1 divisible by 4)", fmt(1, [10 ** 9 - 1]))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), 50), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), 10 ** 9), 30)
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
