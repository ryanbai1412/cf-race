from genlib import *  # noqa: F401,F403

CHECKER = "Unique minimum integer; exact token comparison."
STATEMENT = "Legend, input (1<=x<=1e18), output present."


def solve(s):
    t = s.split()[0]
    out = []
    for i, ch in enumerate(t):
        d = int(ch)
        inv = 9 - d
        out.append(str(inv) if inv < d and not (i == 0 and inv == 0) else ch)
    return "".join(out) + "\n"


def cases(g):
    out = [("boundary", "x=1", fmt(1)), ("boundary", "x=9 (leading 9 stays)", fmt(9)), ("boundary", "x=5 inverts to 4", fmt(5)),
           ("adversarial", "leading 9 followed by 9s", fmt(99999)), ("adversarial", "x=90 (zero stays)", fmt(90)),
           ("adversarial", "all digits 5..9", fmt(956789)),
           ("maxSize", "x=1e18", fmt(10 ** 18)), ("maxSize", "18 nines", fmt(10 ** 18 - 1)), ("maxSize", "18 digits random", fmt(g.randint(10 ** 17, 10 ** 18 - 1)))]
    out += fill(g, lambda g: fmt(g.randint(1, 10 ** g.randint(1, 18))), 90)
    out += fill(g, lambda g: fmt(g.randint(1, 1000)), 30, reason="small")
    return out
