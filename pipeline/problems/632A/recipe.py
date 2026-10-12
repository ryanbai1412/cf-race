from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (each buyer takes half, odd counts get half an apple free), input (1<=n<=40, even 2<=p<=1000, ends at zero apples), output present."


def solve(s):
    t = s.split()
    n, p = int(t[0]), int(t[1])
    apples, money = 0, 0
    for w in reversed(t[2:2 + n]):
        apples = 2 * apples + (w == "halfplus")
        money += apples * p // 2
    return f"{money}\n"


def make(g, n, p, q=0.5):
    return fmt([n, p], *["halfplus" if g.random() < q else "half" for _ in range(n - 1)], "halfplus")


def cases(g):
    out = [("boundary", "n=1 p=2", fmt([1, 2], "halfplus")), ("boundary", "n=1 p=1000", fmt([1, 1000], "halfplus")),
           ("adversarial", "n=40 all halfplus p=1000 (needs 64-bit)", fmt([40, 1000], *["halfplus"] * 40)),
           ("maxSize", "n=40 half then halfplus", fmt([40, 1000], *["half"] * 39, "halfplus")), ("maxSize", "n=40 random", make(g, 40, 998))]
    out += fill(g, lambda g: make(g, g.randint(1, 12), 2 * g.randint(1, 500)), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 40), 2 * g.randint(1, 500), g.random()), 30)
    return out
