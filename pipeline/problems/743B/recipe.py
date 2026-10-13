from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (recursive sequence, find k-th element), input (1<=n<=50, 1<=k<=2^n-1), output present."


def solve(s):
    n, k = ints(s)
    return f"{(k & -k).bit_length()}\n"


def cases(g):
    out = [("boundary", "n=1 k=1", fmt([1, 1])), ("boundary", "n=50 k=2^49 (middle)", fmt([50, 2 ** 49])), ("boundary", "n=50 k=max", fmt([50, 2 ** 50 - 1])),
           ("adversarial", "n=50 k=2^48", fmt([50, 2 ** 48])), ("adversarial", "n=50 k=3*2^48", fmt([50, 3 * 2 ** 48])),
           ("maxSize", "n=50 k=2^50-2", fmt([50, 2 ** 50 - 2]))]
    out += [("random", "n=4 every k", fmt([4, k])) for k in range(1, 16)]
    out += fill(g, lambda g: fmt([(n := g.randint(1, 50)), g.randint(1, 2 ** n - 1)]), 60)
    out += fill(g, lambda g: fmt([50, g.randint(1, 2 ** 20) << g.randint(0, 29)]), 30, reason="power-of-two-heavy")
    return out
