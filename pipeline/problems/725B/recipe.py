from genlib import *  # noqa: F401,F403

CHECKER = "Single integer (up to ~6e18, 64-bit); unique, exact token comparison."
STATEMENT = "Legend (two attendants serving rows 1&3, 2&4, then 5&7 ... in seat order f e d a b c), input ('ns', 1<=n<=1e18), output present."
ORDER = {"f": 1, "e": 2, "d": 3, "a": 4, "b": 5, "c": 6}


def solve(s):
    t = s.split()[0]
    return f"{wait(int(t[:-1]), t[-1])}\n"


def wait(n, seat):
    k = (n - 1) // 4
    pos = (n - 1) % 4
    t = k * 16
    if pos in (1, 3):
        t += 7
    return t + ORDER[seat]


def cases(g):
    E = 10 ** 18
    out = [("boundary", "1f", fmt("1f")), ("boundary", "1c", fmt("1c")), ("boundary", "1e18 c", fmt(f"{E}c")),
           ("adversarial", "rows 1..8 all seats", fmt("8a")), ("adversarial", "row 3 (served with 1)", fmt("3d")),
           ("maxSize", "1e18-1 f", fmt(f"{E - 1}f")), ("maxSize", "1e18-2 a", fmt(f"{E - 2}a"))]
    out += [("random", "rows 1..20 every seat", fmt(f"{r}{c}")) for r in range(1, 21) for c in "abcdef"]
    out += fill(g, lambda g: fmt(f"{g.randint(1, E)}{g.choice('abcdef')}"), 30)
    return out
