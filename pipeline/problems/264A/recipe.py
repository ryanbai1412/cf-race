from genlib import *  # noqa: F401,F403

CHECKER = "Permutation of stone numbers in left-to-right order; unique, exact token comparison."
STATEMENT = "Legend (stone falls at centre, escape l/r), input (string of l/r, 1<=|s|<=1e6), output present."


def solve(s):
    t = s.split()[0]
    r = [i for i, c in enumerate(t, 1) if c == "r"]
    l = [i for i, c in enumerate(t, 1) if c == "l"]
    return "".join(f"{i}\n" for i in r + l[::-1])


def word(g, n):
    return "".join(g.choice("lr") for _ in range(n))


def cases(g):
    out = [("boundary", "single l", fmt("l")), ("boundary", "single r", fmt("r")),
           ("adversarial", "alternating", fmt("lrlrlrlr")),
           ("maxSize", "1e6 l (reverse order output)", fmt("l" * 10 ** 6)), ("maxSize", "1e6 random", fmt(word(g, 10 ** 6)))]
    out += fill(g, lambda g: fmt(word(g, g.randint(1, 12))), 85, reason="small random")
    out += fill(g, lambda g: fmt(word(g, g.randint(13, 3000))), 30)
    return out
