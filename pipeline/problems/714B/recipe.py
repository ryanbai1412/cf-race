from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (add/subtract one x to make all equal), input (1<=n<=1e5, 0<=ai<=1e9), output present."


def solve(s):
    v = sorted(set(ints(s)[1:]))
    if len(v) <= 2 or (len(v) == 3 and v[0] + v[2] == 2 * v[1]):
        return "YES\n"
    return "NO\n"


def make(g, n, pool):
    return fmt(n, [g.choice(pool) for _ in range(n)])


def pool(g):
    a, d = g.randint(0, 10), g.randint(0, 5)
    return [a, a + d, a + 2 * d + g.choice([0, 0, 1, -1])] + ([a + 3 * d + 1] if g.random() < 0.2 else [])


def cases(g):
    N, E = 10 ** 5, 10 ** 9
    out = [("boundary", "n=1", fmt(1, [E])), ("boundary", "two distinct", fmt(2, [0, E])),
           ("adversarial", "three values not arithmetic", fmt(3, [1, 2, 4])), ("adversarial", "three arithmetic extremes", fmt(3, [0, 5 * 10 ** 8, E])),
           ("adversarial", "four distinct", fmt(4, [1, 2, 3, 4])),
           ("maxSize", "n=1e5 three arithmetic", make(g, N, [0, 5 * 10 ** 8, E])), ("maxSize", "n=1e5 random", make(g, N, list(range(0, E, 10 ** 7)))),
           ("maxSize", "n=1e5 three off by one", make(g, N, [1, 3, 6]))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), pool(g)), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), pool(g)), 25)
    return out
