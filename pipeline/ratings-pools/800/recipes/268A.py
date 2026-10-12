from rlib import *

CONSTRAINTS = "n in 2..30, then n pairs of distinct integers h_i, a_i in 1..100."
UNIQUENESS = "Count is a unique integer."
STATEMENT = "Reviewed full statement: count ordered pairs (i,j), i != j, with h_i == a_j."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 2, 30)
    need(len(ls) == n + 1, "n lines")
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 2, "pair")
        h, a = nums(p, 1, 100)
        need(h != a, "distinct colors")


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]
    h, a = t[1::2], t[2::2]
    return str(sum(h[i] == a[j] for i in range(n) for j in range(n) if i != j))


def extra():
    rows = "".join(f"{1 + i % 2} {2 - i % 2}\n" for i in range(30))
    return [("boundary", "n=2 no clashes", "2\n1 2\n3 4\n"), ("boundary", "n=2 both clash", "2\n1 2\n2 1\n"),
            ("adversarial", "same team pair excluded", "3\n1 2\n3 1\n5 6\n"),
            ("maxSize", "n=30 alternating 1/2 colors (450 clashes)", "30\n" + rows),
            ("maxSize", "n=30 max colors", "30\n" + "".join(f"100 {99 - i}\n" for i in range(30)))]
