from genlib import *  # noqa: F401,F403

CHECKER = "Count then increasing index list; the set is unique, exact token comparison (empty second line optional)."
STATEMENT = "Legend, input (2<=n<=2e5, 1<=ai<=1000), output present."


def solve(s):
    v = ints(s)
    n, a = v[0], v[1:]
    t = sum(a)
    idx = [i for i, x in enumerate(a, 1) if x * n == t]
    return f"{len(idx)}\n" + (" ".join(map(str, idx)) + "\n" if idx else "")


def arr(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    out = [("boundary", "n=2 equal", fmt(2, [1, 1])), ("boundary", "n=2 different (0)", fmt(2, [1, 2])),
           ("adversarial", "mean is non-integer", fmt(3, [1, 1, 2])),
           ("adversarial", "single element equals mean", fmt(5, [1, 2, 3, 4, 5])),
           ("maxSize", "n=2e5 all 1000 (all indices)", fmt(200000, [1000] * 200000)),
           ("maxSize", "n=2e5 random", arr(g, 200000, 1000))]
    out += fill(g, lambda g: arr(g, g.randint(2, 8), 3), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(2, 2000), g.choice([2, 1000])), 30)
    return out
