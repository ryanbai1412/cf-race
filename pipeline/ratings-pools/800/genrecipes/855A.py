from rlib import *

CONSTRAINTS = "n in 1..100; n lowercase names of length 1..100."
UNIQUENESS = "YES/NO per line; checker is case-insensitive per statement, we emit uppercase."
STATEMENT = "Reviewed full statement: YES iff the name appeared earlier."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    need(len(ls) == n + 1, "n names")
    for s in ls[1:]:
        word(s, LOWER, 1, 100)


def solve(inp):
    seen, out = set(), []
    for s in lines(inp)[1:]:
        out.append(yn(s in seen)); seen.add(s)
    return "\n".join(out)


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100]); k = rng.randint(1, 3)
    return f"{n}\n" + "\n".join("".join(rng.choice(LOWER[:k]) for _ in range(rng.choice([1, 2, rng.randint(1, 100)]))) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single name", "1\na\n"), ("adversarial", "prefix is not equal", "3\nab\na\nab\n"),
            ("maxSize", "100 names of length 100", "100\n" + "\n".join(chr(97 + i % 3) * 100 for i in range(100)) + "\n")]
