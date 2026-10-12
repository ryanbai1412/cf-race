from rlib import *

CONSTRAINTS = "one nonempty lowercase string of length <= 10."
UNIQUENESS = "The lexicographically largest palindromic subsequence is unique."
STATEMENT = "Reviewed full statement: answer is the maximum letter repeated its count times."


def validate(inp):
    word(exact_tokens(inp, 1)[0], LOWER, 1, 10)


def solve(inp):
    s = inp.split()[0]
    m = max(s)
    return m * s.count(m)


def brute(s):
    from itertools import combinations
    best = ""
    for r in range(1, len(s) + 1):
        for c in combinations(s, r):
            t = "".join(c)
            if t == t[::-1] and t > best:
                best = t
    return best


def extra():
    r = rng(202)
    out = [("boundary", "single letter", "a\n"), ("adversarial", "longer palindrome with smaller letters loses", "abacabazz\n"),
           ("adversarial", "max letter appears once among repeated smaller letters", "aaaaaaaaaz\n"),
           ("maxSize", "length 10 all z", "z" * 10 + "\n")]
    for i in range(6):
        s = "".join(r.choice("xyz") for _ in range(10))
        assert solve(s) == brute(s)
        out.append(("maxSize", f"random length-10 over xyz #{i}, brute-force verified", s + "\n"))
    return out
