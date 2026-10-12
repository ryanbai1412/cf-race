from rlib import *

CONSTRAINTS = "n in 2..10^4; n lines of two 0/1 integers."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: make all left doors equal and all right doors equal with minimum flips."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 2, 10000)
    need(len(ls) == n + 1, "n lines")
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 2, "pair")
        nums(p, 0, 1)


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]; l = sum(t[1::2]); r = sum(t[2::2])
    return str(min(l, n - l) + min(r, n - r))


def gen(rng):
    n = rng.choice([2, rng.randint(2, 100), rng.randint(2, 10000), 10000])
    pl, pr = rng.random(), rng.random()
    return f"{n}\n" + "".join(f"{int(rng.random() < pl)} {int(rng.random() < pr)}\n" for _ in range(n))


def extra():
    return [("boundary", "n=2 already uniform", "2\n0 0\n0 0\n"), ("adversarial", "even split both sides", "4\n0 1\n1 0\n0 1\n1 0\n"),
            ("maxSize", "n=10000 all open", "10000\n" + "1 1\n" * 10000)]
