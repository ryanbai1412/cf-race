from rlib import *

CONSTRAINTS = "n in 1..1000; a_i in 1..1000; valid concatenation of 1..x runs (a_1 = 1, a_i = 1 or a_{i-1} + 1)."
UNIQUENESS = "Unique decomposition."
STATEMENT = "Reviewed full statement: count stairways and print each length in order."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n numbers")
    a = nums(a, 1, 1000)
    need(a[0] == 1 and all(a[i] in (1, a[i - 1] + 1) for i in range(1, n)), "valid sequence")


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    runs = [a[i - 1] for i in range(1, len(a)) if a[i] == 1] + [a[-1]]
    return f"{len(runs)}\n{joined(runs)}"


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 1000), 1000])
    a = []
    while len(a) < n:
        a += list(range(1, min(rng.choice([1, 2, rng.randint(1, 50), 1000]), n - len(a)) + 1))
    return f"{n}\n{joined(a)}\n"


def extra():
    return [("boundary", "single step", "1\n1\n"), ("adversarial", "all ones", "4\n1 1 1 1\n"),
            ("maxSize", "one 1000-step stairway", "1000\n" + joined(range(1, 1001)) + "\n")]
