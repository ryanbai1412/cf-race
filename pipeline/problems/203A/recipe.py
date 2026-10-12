from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO decision; unique, exact token comparison."
STATEMENT = "Legend (either problem may be unsolved, submit at minute 0..t-1), input with non-negative-cost guarantee, output present."


def solve(s):
    x, t, a, b, da, db = ints(s)
    pa = {0} | {a - i * da for i in range(t)}
    pb = {0} | {b - j * db for j in range(t)}
    return ("YES" if any(x - p in pb for p in pa) else "NO") + "\n"


def rand(g, xhi=600):
    t = g.randint(1, 300)
    da, db = g.randint(1, 300), g.randint(1, 300)
    a = g.randint(max(1, (t - 1) * da), 300) if (t - 1) * da <= 300 else None
    b = g.randint(max(1, (t - 1) * db), 300) if (t - 1) * db <= 300 else None
    if a is None or b is None:
        t = g.randint(1, 10)
        da, db = g.randint(1, 300 // max(1, t - 1)), g.randint(1, 300 // max(1, t - 1))
        a, b = g.randint(max(1, (t - 1) * da), 300), g.randint(max(1, (t - 1) * db), 300)
    return fmt([g.randint(0, xhi), t, a, b, da, db])


def cases(g):
    out = [("boundary", "x=0 always reachable", fmt([0, 1, 1, 1, 1, 1])),
           ("boundary", "t=1 both solved at minute 0", fmt([600, 1, 300, 300, 300, 300])),
           ("boundary", "x equals the cost at the last minute", fmt([1, 300, 300, 300, 1, 1])),
           ("adversarial", "x just above reachable sum", fmt([601 - 1, 2, 300, 299, 1, 1])),
           ("adversarial", "cost reaches 0 at last minute (only problem A counted)", fmt([3, 4, 3, 300, 1, 100])),
           ("adversarial", "x reachable only by one problem alone", fmt([150, 300, 299, 300, 1, 1])),
           ("maxSize", "t=300 da=db=1 large x", fmt([599, 300, 300, 300, 1, 1])),
           ("maxSize", "t=300 x=600 unreachable after minute 0 combos", fmt([600, 300, 300, 299, 1, 1]))]
    out += fill(g, rand, 80)
    out += fill(g, lambda g: rand(g, 40), 40, reason="small x")
    return out
