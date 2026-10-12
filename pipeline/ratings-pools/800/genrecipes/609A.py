from rlib import *

CONSTRAINTS = "n in 1..100; m in 1..10^5; n capacities in 1..1000 one per line; sum >= m."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: fewest drives (largest first) whose capacity sum reaches m."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    m = num(ls[1], 1, 100000)
    need(len(ls) == n + 2, "n drives")
    need(sum(nums(ls[2:], 1, 1000)) >= m, "answer exists")


def solve(inp):
    t = list(map(int, inp.split()))
    m, s, k = t[1], 0, 0
    for a in sorted(t[2:], reverse=True):
        s += a; k += 1
        if s >= m:
            break
    return str(k)


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    a = [rng.randint(1, rng.choice([1, 10, 1000])) for _ in range(n)]
    m = rng.randint(1, min(100000, sum(a)))
    return f"{n}\n{m}\n" + "\n".join(map(str, a)) + "\n"


def extra():
    return [("boundary", "single drive exactly fits", "1\n1000\n1000\n"), ("adversarial", "needs every drive", "3\n6\n1\n2\n3\n"),
            ("maxSize", "n=100 m=10^5 all 1000", "100\n100000\n" + "1000\n" * 100)]
