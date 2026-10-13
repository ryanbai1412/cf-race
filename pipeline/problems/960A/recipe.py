from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (a^x b^y c^z with z equal to x or y, x,y>=1), input (1<=|S|<=5000 over abc), output present."


def solve(s):
    t = s.split()[0]
    x = len(t) - len(t.lstrip("a"))
    r = t[x:]
    y = len(r) - len(r.lstrip("b"))
    z = r[y:]
    ok = x >= 1 and y >= 1 and z == "c" * len(z) and len(z) in (x, y) and len(z) >= 1
    return "YES\n" if ok else "NO\n"


def make(g, maxlen):
    x, y = g.randint(0, maxlen), g.randint(0, maxlen)
    z = g.choice([x, y, g.randint(0, maxlen)])
    t = "a" * x + "b" * y + "c" * z
    if t and g.random() < 0.3:
        i = g.randrange(len(t))
        t = t[:i] + g.choice("abc") + t[i + 1:]
    return fmt(t or "c")


def cases(g):
    out = [("boundary", "single c", fmt("c")), ("boundary", "abc", fmt("abc")), ("boundary", "a", fmt("a")),
           ("adversarial", "no c", fmt("aabb")), ("adversarial", "no a", fmt("bbcc")), ("adversarial", "out of order", fmt("abcac")),
           ("maxSize", "len 5000 valid", fmt("a" * 2000 + "b" * 1000 + "c" * 2000)), ("maxSize", "len 5000 invalid", fmt("a" * 2500 + "b" * 2499 + "c"))]
    out += fill(g, lambda g: make(g, 7), 110, reason="small random")
    out += fill(g, lambda g: make(g, 1666), 25)
    return out
