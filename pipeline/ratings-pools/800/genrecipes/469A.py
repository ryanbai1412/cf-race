from rlib import *

CONSTRAINTS = "n in 1..100; two lines: p in 0..n then p distinct levels in 1..n."
UNIQUENESS = "Fixed phrase."
STATEMENT = "Reviewed full statement: union covers 1..n."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    n = num(ls[0], 1, 100)
    for l in ls[1:]:
        a = l.split(" ")
        p = num(a[0], 0, n)
        need(len(a) == p + 1, "p levels")
        need(len(set(nums(a[1:], 1, n))) == p, "distinct")


def solve(inp):
    ls = lines(inp)
    n = int(ls[0]); got = set()
    for l in ls[1:]:
        got.update(map(int, l.split()[1:]))
    return "I become the guy." if len(got) == n else "Oh, my keyboard!"


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    def part():
        lv = rng.sample(range(1, n + 1), rng.randint(0, n))
        return " ".join(map(str, [len(lv)] + lv))
    return f"{n}\n{part()}\n{part()}\n"


def extra():
    return [("boundary", "both empty", "1\n0\n0\n"), ("boundary", "one covers all", "3\n3 1 2 3\n0\n"),
            ("adversarial", "level n missing", "4\n2 1 2\n2 2 3\n"),
            ("maxSize", "n=100 both full", "100\n100 " + joined(range(1, 101)) + "\n100 " + joined(range(100, 0, -1)) + "\n")]
