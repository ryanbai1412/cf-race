from rlib import *

CONSTRAINTS = "n in 3..100; d_i in 1..100; 1 <= s,t <= n (may be equal)."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: shorter arc between s and t on a circle."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    n = num(ls[0], 3, 100)
    d = ls[1].split(" ")
    need(len(d) == n, "n distances")
    nums(d, 1, 100)
    st = ls[2].split(" ")
    need(len(st) == 2, "s t")
    nums(st, 1, n)


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]; d = t[1:n + 1]; s, e = sorted(t[n + 1:n + 3])
    one = sum(d[s - 1:e - 1])
    return str(min(one, sum(d) - one))


def gen(rng):
    n = rng.choice([3, rng.randint(3, 100), 100])
    s, e = rng.randint(1, n), rng.randint(1, n)
    return f"{n}\n" + joined(rng.randint(1, rng.choice([1, 100])) for _ in range(n)) + f"\n{s} {e}\n"


def extra():
    return [("boundary", "s equals t", "3\n1 2 3\n2 2\n"), ("adversarial", "s > t, wrap is shorter", "4\n1 100 100 1\n4 1\n"),
            ("maxSize", "n=100 max distances", "100\n" + joined([100] * 100) + "\n1 51\n")]
