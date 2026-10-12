from rlib import *

CONSTRAINTS = "n in 1..150; each statement is one of ++X, X++, --X, X--."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: final value of x starting at 0."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 150)
    need(len(ls) == n + 1, "n statements")
    need(all(s in ("++X", "X++", "--X", "X--") for s in ls[1:]), "statement form")


def solve(inp):
    return str(sum(1 if "+" in s else -1 for s in lines(inp)[1:]))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 150), 150])
    return f"{n}\n" + "\n".join(rng.choice(("++X", "X++", "--X", "X--")) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single postfix decrement", "1\nX--\n"), ("adversarial", "all four forms cancel", "4\n++X\nX--\nX++\n--X\n"),
            ("maxSize", "n=150 all decrement", "150\n" + "--X\n" * 150)]
