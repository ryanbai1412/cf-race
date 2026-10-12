from rlib import *

CONSTRAINTS = "n in 1..100; n lowercase words of length 1..100, one per line."
UNIQUENESS = "Each abbreviation is determined."
STATEMENT = "Reviewed full statement: words longer than 10 become first+count+last."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    need(len(ls) == n + 1, "n words")
    for w in ls[1:]:
        word(w, LOWER, 1, 100)


def solve(inp):
    return "\n".join(w if len(w) <= 10 else f"{w[0]}{len(w) - 2}{w[-1]}" for w in lines(inp)[1:])


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    ws = ["".join(rng.choice(LOWER) for _ in range(rng.choice([1, 10, 11, rng.randint(1, 100), 100]))) for _ in range(n)]
    return f"{n}\n" + "\n".join(ws) + "\n"


def extra():
    return [("boundary", "length exactly 10 and 11", "2\nabcdefghij\nabcdefghijk\n"), ("boundary", "single letter", "1\nz\n"),
            ("adversarial", "length 12 gives two-digit-free count", "1\naaaaaaaaaaaa\n"),
            ("maxSize", "100 words of length 100", "100\n" + "\n".join(["q" * 100] * 100) + "\n")]
