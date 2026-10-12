from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO decision; unique, exact token comparison (case as in statement)."
STATEMENT = "Legend, input (1<=n<=1000), output present in the pinned source row."


def solve(s):
    n = int(s)
    seen, pos = {0}, 0
    for k in range(1, 2 * n + 1):
        pos = (pos + k) % n
        seen.add(pos)
    return ("YES" if len(seen) == n else "NO") + "\n"


def cases(g):
    out = [("boundary", "n=1", fmt(1)), ("boundary", "n=2", fmt(2)), ("boundary", "n=3", fmt(3)),
           ("adversarial", "n=512 largest power of two in range", fmt(512)), ("adversarial", "n=511", fmt(511)),
           ("adversarial", "n=513", fmt(513)), ("adversarial", "n=384 (3*128)", fmt(384)),
           ("maxSize", "n=1000 maximum", fmt(1000)), ("maxSize", "n=999", fmt(999))]
    out += [("random", "power of two", fmt(1 << k)) for k in range(10)]
    out += [("random", "random n", fmt(n)) for n in g.sample(range(1, 1001), 120)]
    return out
