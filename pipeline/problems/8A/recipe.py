from genlib import *  # noqa: F401,F403

CHECKER = "One of forward/backward/both/fantasy; unique, exact token comparison."
STATEMENT = "Legend (two ordered non-overlapping substrings forward/reverse), input (|s|<=1e5, |a|,|b|<=100 lowercase), output present."


def ok(s, a, b):
    i = s.find(a)
    return i >= 0 and s.find(b, i + len(a)) >= 0


def solve(t):
    s, a, b = t.split()
    f, r = ok(s, a, b), ok(s[::-1], a, b)
    return ("both" if f and r else "forward" if f else "backward" if r else "fantasy") + "\n"


def w(g, n, al):
    return "".join(g.choice(al) for _ in range(n))


def make(g, n, al):
    s = w(g, n, al)
    pick = lambda: s[(i := g.randrange(n)):i + g.randint(1, min(100, n - i))] if g.random() < 0.7 else w(g, g.randint(1, 3), al)
    return fmt(s, pick(), pick())


def cases(g):
    N = 10 ** 5
    out = [("boundary", "single letters", fmt("a", "a", "a")), ("boundary", "sample", fmt("atob", "a", "b")),
           ("adversarial", "overlap not allowed", fmt("aaa", "aa", "aa")), ("adversarial", "palindrome both", fmt("abcba", "ab", "a")),
           ("maxSize", "1e5 a with 100-length patterns", fmt("a" * N, "a" * 100, "a" * 100)), ("maxSize", "1e5 random ab", make(g, N, "ab"))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), "ab"), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(11, 5000), "abc"), 25)
    return out
