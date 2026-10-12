from rlib import *

CONSTRAINTS = "Exactly three lines, each 1..100 chars of lowercase letters and spaces with at least one letter."
UNIQUENESS = "Decision problem."
STATEMENT = "Reviewed full statement: vowel counts (aeiou) of the three phrases are 5, 7, 5."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three phrases")
    for s in ls:
        word(s, LOWER + " ", 1, 100)
        need(s.strip() != "", "non-space character")


def solve(inp):
    return yn([sum(c in "aeiou" for c in s) for s in lines(inp)] == [5, 7, 5])


def gen(rng):
    out = []
    for target in (5, 7, 5):
        k = target if rng.random() < 0.7 else rng.randint(0, 9)
        parts = [rng.choice("aeiou") for _ in range(k)] + [rng.choice("bcdfghjklmnpqrstvwxyz") for _ in range(rng.randint(1, 30))]
        rng.shuffle(parts)
        s = "".join(c if rng.random() > 0.15 else c + " " * rng.randint(1, 3) for c in parts)
        s = " " * rng.randint(0, 2) + s + " " * rng.randint(0, 2)
        out.append(s[:100] if s[:100].strip() else "b")
    return "\n".join(out) + "\n"


def extra():
    return [("boundary", "single-letter lines", "b\nc\nd\n"), ("adversarial", "leading/trailing and multiple spaces", "  aeiou \nae  io u ae \n aeiou\n"),
            ("maxSize", "100-char lines", ("aeiou" + "b" * 95) + "\n" + ("aeiouae" + " " * 93) + "\n" + (" " * 95 + "aeiou") + "\n")]
