from rlib import *

CONSTRAINTS = "n in 2..100, k in 1..n-1; string of n chars over '.#GT' with exactly one G and one T."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: jumps of exactly k onto empty cells only."


def validate(inp):
    t = exact_tokens(inp, 3)
    n = num(t[0], 2, 100); num(t[1], 1, n - 1)
    word(t[2], ".#GT", n, n)
    need(t[2].count("G") == 1 and t[2].count("T") == 1, "one G and one T")


def solve(inp):
    _, k, s = inp.split()
    k = int(k)
    g, t = sorted((s.index("G"), s.index("T")))
    if (t - g) % k:
        return "NO"
    return yn(all(s[i] != "#" for i in range(g, t + 1, k)))


def extra():
    return [("boundary", "n=2 k=1 adjacent", "2 1\nGT\n"), ("boundary", "n=2 k=1 reversed", "2 1\nTG\n"),
            ("adversarial", "obstacle on a jump landing", "5 2\nG.#.T\n"), ("adversarial", "obstacle skipped over", "5 2\nG#.#T\n"),
            ("maxSize", "n=100 k=99 ends", "100 99\nG" + "#" * 98 + "T\n"),
            ("maxSize", "n=100 k=3 misaligned", "100 3\nG" + "." * 97 + "T.\n")]
