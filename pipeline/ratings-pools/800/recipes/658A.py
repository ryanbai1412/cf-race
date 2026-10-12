from rlib import *

CONSTRAINTS = "n in 1..50, c in 1..1000; strictly increasing p_i in 1..1000; strictly increasing t_i in 1..1000."
UNIQUENESS = "One of three fixed outcomes."
STATEMENT = "Reviewed full statement: sum max(0, p_i - c*time) for both orders."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    a = ls[0].split(" ")
    need(len(a) == 2, "n c")
    n = num(a[0], 1, 50); num(a[1], 1, 1000)
    for l in ls[1:]:
        v = nums(l.split(" "), 1, 1000)
        need(len(v) == n and all(v[i] < v[i + 1] for i in range(n - 1)), "strictly increasing n values")


def solve(inp):
    t = list(map(int, inp.split()))
    n, c = t[0], t[1]
    p, tm = t[2:2 + n], t[2 + n:]

    def score(order):
        x = s = 0
        for i in order:
            x += tm[i]
            s += max(0, p[i] - c * x)
        return s

    a, b = score(range(n)), score(range(n - 1, -1, -1))
    return "Limak" if a > b else "Radewoosh" if b > a else "Tie"


def extra():
    return [("boundary", "n=1 tie", "1 1\n10\n1\n"), ("boundary", "n=1 both zero", "1 1000\n1\n1\n"),
            ("adversarial", "all scores clamp to zero -> Tie", "3 1000\n1 2 3\n1 2 3\n"),
            ("maxSize", "n=50 c=1", "50 1\n" + joined(range(951, 1001)) + "\n" + joined(range(1, 51)) + "\n"),
            ("maxSize", "n=50 c=2 wide spread", "50 2\n" + joined(range(20, 1001, 20)) + "\n" + joined(range(1, 51)) + "\n")]
