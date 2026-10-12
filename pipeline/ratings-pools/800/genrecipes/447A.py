from rlib import *

CONSTRAINTS = "p, n in 2..300; n lines with x_i in 0..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: first insertion index colliding mod p, else -1."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "p n")
    _, n = num(p[0], 2, 300), num(p[1], 2, 300)
    need(len(ls) == n + 1, "n values")
    nums(ls[1:], 0, 10 ** 9)


def solve(inp):
    t = list(map(int, inp.split()))
    p, seen = t[0], set()
    for i, x in enumerate(t[2:], 1):
        if x % p in seen:
            return str(i)
        seen.add(x % p)
    return "-1"


def gen(rng):
    p = rng.choice([2, rng.randint(2, 300), 300]); n = rng.choice([2, rng.randint(2, 300), 300])
    if rng.random() < 0.4:
        xs = rng.sample(range(p), min(n, p))
        xs += [rng.randint(0, 10 ** 9) for _ in range(n - len(xs))]
    else:
        xs = [rng.randint(0, 10 ** 9) for _ in range(n)]
    return f"{p} {n}\n" + "\n".join(map(str, xs)) + "\n"


def extra():
    return [("boundary", "p=2 collision at second insertion", "2 2\n0\n2\n"), ("boundary", "no conflict", "10 2\n0\n1\n"),
            ("adversarial", "collision only via 10^9 mod p", "7 3\n6\n1000000000\n5\n"),
            ("maxSize", "p=n=300 permutation of residues", "300 300\n" + "\n".join(str(10 ** 9 - i) for i in range(300)) + "\n")]
