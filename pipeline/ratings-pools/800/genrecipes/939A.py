from rlib import *

CONSTRAINTS = "n in 2..5000; f_i in 1..n with f_i != i."
UNIQUENESS = "Decision problem."
STATEMENT = "Reviewed full statement: YES iff some i has f(f(f(i))) = i."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 2, 5000)
    f = ls[1].split(" ")
    need(len(f) == n, "n values")
    need(all(v != i + 1 for i, v in enumerate(nums(f, 1, n))), "f_i != i")


def solve(inp):
    f = [0] + list(map(int, inp.split()))[1:]
    return yn(any(f[f[f[i]]] == i for i in range(1, len(f))))


def gen(rng):
    n = rng.choice([2, 3, 4, rng.randint(2, 100), rng.randint(2, 5000)])
    f = []
    for i in range(1, n + 1):
        v = rng.randint(1, n - 1)
        f.append(v + (v >= i))
    return f"{n}\n{joined(f)}\n"


def extra():
    return [("boundary", "n=2 mutual", "2\n2 1\n"), ("adversarial", "4-cycle is not a triangle", "4\n2 3 4 1\n"),
            ("maxSize", "n=5000 long cycle", "5000\n" + joined(list(range(2, 5001)) + [1]) + "\n")]
