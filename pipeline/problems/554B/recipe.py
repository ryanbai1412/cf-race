from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (sweep whole columns), input (1<=n<=100, n binary strings of length n), output present."


def solve(s):
    rows = s.split()[1:]
    c = {}
    for r in rows:
        c[r] = c.get(r, 0) + 1
    return f"{max(c.values())}\n"


def make(g, n, k):
    pool = ["".join(g.choice("01") for _ in range(n)) for _ in range(k)]
    return fmt(n, *[g.choice(pool) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=1 dirty", fmt(1, "0")), ("boundary", "n=1 clean", fmt(1, "1")),
           ("adversarial", "complementary rows are different patterns", fmt(2, "01", "10")),
           ("maxSize", "n=100 all identical", make(g, 100, 1)), ("maxSize", "n=100 all distinct rows", make(g, 100, 100)),
           ("maxSize", "n=100 few patterns", make(g, 100, 3))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 8)), g.randint(1, n)), 80, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(1, 100)), g.randint(1, n)), 30)
    return out
