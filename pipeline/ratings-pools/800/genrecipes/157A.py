from rlib import *

CONSTRAINTS = "n in 1..30; n rows of n integers in 1..100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count cells with column sum > row sum."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 30)
    need(len(ls) == n + 1, "n rows")
    for r in ls[1:]:
        p = r.split(" ")
        need(len(p) == n, "n values")
        nums(p, 1, 100)


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]; g = [t[1 + i * n:1 + (i + 1) * n] for i in range(n)]
    rs = [sum(r) for r in g]; cs = [sum(g[i][j] for i in range(n)) for j in range(n)]
    return str(sum(cs[j] > rs[i] for i in range(n) for j in range(n)))


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 30), 30])
    hi = rng.choice([1, 2, 100])
    return f"{n}\n" + "\n".join(joined(rng.randint(1, hi) for _ in range(n)) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=1", "1\n1\n"), ("adversarial", "all equal -> 0", "3\n7 7 7\n7 7 7\n7 7 7\n"),
            ("maxSize", "n=30 max values", "30\n" + "\n".join(joined([100] * 30) for _ in range(30)) + "\n")]
