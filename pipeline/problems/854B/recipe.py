from genlib import *  # noqa: F401,F403

CHECKER = "Two integers; unique, exact token comparison."
STATEMENT = "Legend (k inhabited of n, min/max good apartments), input (1<=n<=1e9, 0<=k<=n), output present."


def solve(s):
    n, k = ints(s)
    lo = 0 if k == 0 or k == n else 1
    return f"{lo} {min(2 * k, n - k)}\n"


def cases(g):
    E = 10 ** 9
    out = [("boundary", "n=1 k=0", fmt([1, 0])), ("boundary", "n=1 k=1", fmt([1, 1])), ("boundary", "k=n max", fmt([E, E])), ("boundary", "k=0 max", fmt([E, 0])),
           ("adversarial", "k=n/3", fmt([9, 3])), ("adversarial", "k=n-1", fmt([E, E - 1])), ("maxSize", "n=1e9 k=333333333", fmt([E, 333333333]))]
    out += [("random", "small exhaustive", fmt([n, k])) for n in range(1, 13) for k in range(0, n + 1)]
    out += fill(g, lambda g: fmt([(n := g.randint(1, E)), g.randint(0, n)]), 40)
    return out
