from genlib import *  # noqa: F401,F403

CHECKER = "Count then ascending values; unique, exact token comparison."
STATEMENT = "Legend (x + digitsum(x) = n), input (1<=n<=1e9), output present."


def solve(s):
    n = int(s)
    xs = [x for x in range(max(1, n - 90), n) if x + sum(map(int, str(x))) == n]
    return "\n".join(map(str, [len(xs)] + xs)) + "\n"


def cases(g):
    E = 10 ** 9
    out = [("boundary", "n=1", fmt(1)), ("boundary", "n=2", fmt(2)), ("boundary", "n=1e9", fmt(E)),
           ("adversarial", "two solutions n=1000000001-? candidate", fmt(101)), ("adversarial", "n=999999999", fmt(999999999)),
           ("maxSize", "n=1e9-1 region", fmt(E - 7))]
    out += [("random", "small n", fmt(n)) for n in range(3, 60)]
    out += fill(g, lambda g: fmt((x := g.randint(1, E - 100)) + sum(map(int, str(x)))), 40, reason="constructed solvable")
    out += fill(g, lambda g: fmt(g.randint(1, E)), 15)
    return [c for c in out if int(c[2]) <= E]
