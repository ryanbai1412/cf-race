from genlib import *  # noqa: F401,F403

CHECKER = "Single stop index; ties broken by closest-to-university; unique, exact token comparison."
STATEMENT = "Legend (cannot leave at stop 1; minimise xi/vb + dist/vs; tie -> closest), input (2<=n<=100, 1<=vb,vs<=1000, 0=x1<...<xn<=1e5, |xu|,|yu|<=1e5), output present."
from decimal import Decimal, getcontext

TIE = Decimal(10) ** -40


def solve(s):
    getcontext().prec = 80
    v = ints(s)
    n, vb, vs = v[0], v[1], v[2]
    x = v[3:3 + n]
    xu, yu = v[3 + n], v[4 + n]
    best = None
    for i in range(1, n):
        d2 = (x[i] - xu) ** 2 + yu * yu
        t = Decimal(x[i] * vs) + vb * Decimal(d2).sqrt()
        if best is None or t < best[0] - TIE or (abs(t - best[0]) <= TIE and d2 < best[1]):
            best = (t, d2, i + 1)
    return f"{best[2]}\n"


def make(g, n, hi=10 ** 5):
    x = [0] + sorted(g.sample(range(1, hi + 1), n - 1))
    return fmt([n, g.randint(1, 1000), g.randint(1, 1000)], x, [g.randint(-hi, hi), g.randint(-hi, hi)])


def cases(g):
    E = 10 ** 5
    out = [("boundary", "n=2", fmt([2, 1, 1], [0, 1], [0, 0])), ("boundary", "university at stop", fmt([3, 5, 2], [0, 4, 9], [4, 0])),
           ("adversarial", "tie in time, choose closest", fmt([3, 1, 1], [0, 3, 4], [4, 1])), ("adversarial", "fast runner", fmt([4, 1, 1000], [0, 1, 2, 3], [E, E])),
           ("maxSize", "n=100 max coords", make(g, 100)), ("maxSize", "n=100 xn=1e5 far university", fmt([100, 1000, 1], list(range(0, 99)) + [E], [-E, -E]))]
    out += fill(g, lambda g: make(g, g.randint(2, 6), 20), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(7, 100)), 25)
    return out
