from genlib import *  # noqa: F401,F403

CHECKER = "Single string; lexicographic minimum is unique; exact token comparison."
STATEMENT = "Legend (shift exactly one non-empty substring back by one letter), input (lowercase, 1<=|s|<=1e5), output present."


def solve(s):
    t = list(s.split()[0])
    i = 0
    while i < len(t) and t[i] == "a":
        i += 1
    if i == len(t):
        t[-1] = "z"
    else:
        while i < len(t) and t[i] != "a":
            t[i] = chr(ord(t[i]) - 1)
            i += 1
    return "".join(t) + "\n"


def word(g, n, alpha="abcdefghijklmnopqrstuvwxyz"):
    return "".join(g.choice(alpha) for _ in range(n))


def cases(g):
    N = 10 ** 5
    out = [("boundary", "single a (must become z)", fmt("a")), ("boundary", "single z", fmt("z")),
           ("adversarial", "all a (last becomes z)", fmt("aaaa")), ("adversarial", "leading a then block", fmt("aabca")),
           ("maxSize", "1e5 a", fmt("a" * N)), ("maxSize", "1e5 b", fmt("b" * N)), ("maxSize", "1e5 random ab", fmt(word(g, N, "ab")))]
    out += fill(g, lambda g: fmt(word(g, g.randint(1, 8), "abz")), 100, reason="small random")
    out += fill(g, lambda g: fmt(word(g, g.randint(9, 5000))), 30)
    return out
