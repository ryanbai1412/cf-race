from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer; unique, exact token comparison."
STATEMENT = "Legend (flip or swap digits), input (two equal-length 4/7 strings, length<=1e5), output present."


def solve(s):
    a, b = s.split()
    x = sum(1 for p, q in zip(a, b) if p == "4" and q == "7")
    y = sum(1 for p, q in zip(a, b) if p == "7" and q == "4")
    return f"{max(x, y)}\n"


def word(g, n):
    return "".join(g.choice("47") for _ in range(n))


def cases(g):
    N = 10 ** 5
    out = [("boundary", "length 1 equal", fmt("4", "4")), ("boundary", "length 1 differ", fmt("4", "7")),
           ("adversarial", "only swaps needed", fmt("4747", "7474")), ("adversarial", "only flips needed", fmt("4444", "7777")),
           ("maxSize", "length 1e5 all different", fmt("4" * N, "7" * N)), ("maxSize", "length 1e5 random", fmt(word(g, N), word(g, N)))]
    out += fill(g, lambda g: (lambda n: fmt(word(g, n), word(g, n)))(g.randint(1, 10)), 80, reason="small random")
    out += fill(g, lambda g: (lambda n: fmt(word(g, n), word(g, n)))(g.randint(10, 3000)), 30)
    return out
