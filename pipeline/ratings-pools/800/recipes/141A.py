from collections import Counter
from rlib import *

CONSTRAINTS = "three nonempty lines of uppercase Latin letters, each of length <= 100."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: pile must be exactly a permutation of guest+host letters."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    for l in ls:
        word(l, UPPER, 1, 100)


def solve(inp):
    a, b, c = lines(inp)[:3]
    return yn(Counter(a + b) == Counter(c))


def extra():
    r = rng(141)
    a = "".join(r.choice(UPPER) for _ in range(100)); b = "".join(r.choice(UPPER) for _ in range(100))
    c = list(a + b); r.shuffle(c); c = "".join(c)
    return [("boundary", "single letters, exact", "A\nB\nBA\n"), ("boundary", "single letters, pile too short", "A\nB\nA\n"),
            ("adversarial", "same multiset size, one letter swapped", "AAB\nC\nAACC\n"),
            ("adversarial", "pile contains all letters plus one extra", "AB\nCD\nABCDD\n"),
            ("maxSize", "length-100 names with pile capped at 100 letters -> NO", f"{a}\n{b}\n{c[:100]}\n"),
            ("maxSize", "length-100 lines all same letter", "Z" * 100 + "\n" + "Z" * 100 + "\n" + "Z" * 100 + "\n")]
