from genlib import *  # noqa: F401,F403

CHECKER = "Single integer string; unique, exact token comparison."
STATEMENT = "Legend (seven-segment digits, at most n segments, max number), input (2<=n<=1e5), output present."


def solve(s):
    n = int(s)
    return ("7" + "1" * ((n - 3) // 2) if n % 2 else "1" * (n // 2)) + "\n"


def cases(g):
    out = [("boundary", "n=2", fmt(2)), ("boundary", "n=3", fmt(3)), ("boundary", "n=1e5", fmt(10 ** 5)),
           ("adversarial", "n=5", fmt(5)), ("adversarial", "n=4", fmt(4)), ("maxSize", "n=99999", fmt(99999))]
    out += [("random", "small n", fmt(n)) for n in range(6, 60)]
    out += fill(g, lambda g: fmt(g.randint(60, 10 ** 5)), 50)
    return out
