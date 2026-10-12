from rlib import *

CONSTRAINTS = "n in 1..100; 0 <= p_i <= q_i <= 100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: rooms with q - p >= 2."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    need(len(ls) == n + 1, "n rooms")
    for l in ls[1:]:
        a = l.split(" ")
        need(len(a) == 2, "p q")
        p, q = nums(a, 0, 100)
        need(p <= q, "p <= q")


def solve(inp):
    t = list(map(int, inp.split()))[1:]
    return str(sum(q - p >= 2 for p, q in zip(t[::2], t[1::2])))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    rows = []
    for _ in range(n):
        q = rng.randint(0, 100)
        rows.append((max(0, q - rng.choice([0, 1, 2, 3, q])), q))
    return f"{n}\n" + "\n".join(f"{p} {q}" for p, q in rows) + "\n"


def extra():
    return [("boundary", "empty zero-capacity room", "1\n0 0\n"), ("adversarial", "free space exactly 1 and 2", "2\n4 5\n4 6\n"),
            ("maxSize", "n=100 empty rooms", "100\n" + "0 100\n" * 100)]
