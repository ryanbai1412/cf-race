from rlib import *

CONSTRAINTS = "Two permutations of 26 lowercase letters; text of 1..1000 letters/digits."
UNIQUENESS = "Unique string."
STATEMENT = "Reviewed full statement: map each letter through layout1 position into layout2, keep case; digits unchanged."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    for s in ls[:2]:
        word(s, LOWER, 26, 26)
        need(len(set(s)) == 26, "permutation")
    word(ls[2], LETTERS + DIGITS, 1, 1000)


def solve(inp):
    a, b, s = lines(inp)
    m = {x: y for x, y in zip(a, b)}
    return "".join(m[c] if c in m else m[c.lower()].upper() if c.lower() in m else c for c in s)


def gen(rng):
    a, b = list(LOWER), list(LOWER)
    rng.shuffle(a); rng.shuffle(b)
    n = rng.choice([1, rng.randint(1, 1000), 1000])
    return "".join(a) + "\n" + "".join(b) + "\n" + "".join(rng.choice(LETTERS + DIGITS) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single digit", LOWER + "\n" + LOWER[::-1] + "\n7\n"), ("adversarial", "uppercase mapping", LOWER + "\n" + LOWER[1:] + "a\nZz9A\n"),
            ("maxSize", "1000 chars", "qwertyuiopasdfghjklzxcvbnm\nveamhjsgqocnrbfxdtwkylupzi\n" + ("Aa0" * 334)[:1000] + "\n")]
