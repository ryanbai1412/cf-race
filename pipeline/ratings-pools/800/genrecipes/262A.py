from rlib import *

CONSTRAINTS = "n, k in 1..100; n integers in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count numbers with at most k digits equal to 4 or 7."


def validate(inp):
    t = toks(inp)
    n, k = num(t[0], 1, 100), num(t[1], 1, 100)
    need(len(t) == n + 2, "n values")
    nums(t[2:], 1, 10 ** 9)


def solve(inp):
    t = inp.split()
    k = int(t[1])
    return str(sum(sum(c in "47" for c in a) <= k for a in t[2:]))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100]); k = rng.choice([1, 2, rng.randint(1, 10), 100])
    vs = []
    for _ in range(n):
        if rng.random() < 0.5:
            vs.append(int("".join(rng.choice("47") for _ in range(rng.randint(1, 9)))))
        else:
            vs.append(rng.randint(1, 10 ** 9))
    return f"{n} {k}\n" + joined(vs) + "\n"


def extra():
    return [("boundary", "k=1 single lucky digit", "1 1\n4\n"), ("boundary", "10^9 has no lucky digits", "1 1\n1000000000\n"),
            ("adversarial", "nine lucky digits vs k=8", "2 8\n474747474 777777777\n"),
            ("maxSize", "n=100 k=100", "100 100\n" + joined([777777777] * 100) + "\n")]
