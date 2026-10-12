from genlib import *  # noqa: F401,F403

CHECKER = "Deterministic resulting string; unique, exact token comparison."
STATEMENT = "Legend defines both operations, input (x/y string, length<=1e6, result non-empty), output present."


def solve(s):
    t = s.split()[0]
    x, y = t.count("x"), t.count("y")
    return ("x" * (x - y) if x > y else "y" * (y - x)) + "\n"


def word(g, n):
    while True:
        w = "".join(g.choice("xy") for _ in range(n))
        if w.count("x") * 2 != n:
            return w


def cases(g):
    out = [("boundary", "single x", fmt("x")), ("boundary", "single y", fmt("y")),
           ("adversarial", "yxyxy", fmt("yxyxy")), ("adversarial", "difference of one", fmt("xy" * 50 + "x")),
           ("maxSize", "1e6 characters all x", fmt("x" * 10 ** 6)), ("maxSize", "1e6 characters near-balanced", fmt("yx" * 499999 + "yy"))]
    out += fill(g, lambda g: fmt(word(g, g.randint(1, 12))), 80, reason="small random")
    out += fill(g, lambda g: fmt(word(g, g.randint(13, 5000))), 30)
    return out
