from rlib import *

CONSTRAINTS = "n in 1..10^5; c in 1..10^9; strictly increasing t_i in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: words reset when gap > c; count after the last word."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n c")
    n = num(p[0], 1, 100000); num(p[1], 1, 10 ** 9)
    t = ls[1].split(" ")
    need(len(t) == n, "n times")
    t = nums(t, 1, 10 ** 9)
    need(all(t[i] < t[i + 1] for i in range(n - 1)), "strictly increasing")


def solve(inp):
    v = list(map(int, inp.split()))
    c, t = v[1], v[2:]
    k = 1
    for i in range(1, len(t)):
        k = k + 1 if t[i] - t[i - 1] <= c else 1
    return str(k)


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 3000)])
    c = rng.choice([1, rng.randint(1, 10), rng.randint(1, 10 ** 9)])
    t = sorted(rng.sample(range(1, 10 ** 9 + 1), n)) if rng.random() < 0.5 else list(range(1, n * 2, 2)) if rng.random() < 0.5 else sorted(rng.sample(range(1, 3 * n + 1), n))
    return f"{n} {c}\n{joined(t)}\n"


def extra():
    return [("boundary", "single word", "1 1\n1000000000\n"), ("adversarial", "gap exactly c keeps words", "3 2\n1 3 6\n"),
            ("maxSize", "n=10^5 all kept", "100000 1\n" + joined(range(1, 100001)) + "\n")]
