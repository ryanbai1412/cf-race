from rlib import *

CONSTRAINTS = "n in 2..10^5; distinct points, |x|, |y| <= 10^9, x != 0."
UNIQUENESS = "Decision problem; we emit 'Yes'/'No'."
STATEMENT = "Reviewed full statement: Yes iff at most one point on one side of OY."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 2, 100000)
    need(len(ls) == n + 1, "n points")
    pts = set()
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 2, "x y")
        x, y = num(p[0], -10 ** 9, 10 ** 9), num(p[1], -10 ** 9, 10 ** 9)
        need(x != 0, "x != 0")
        pts.add((x, y))
    need(len(pts) == n, "distinct")


def solve(inp):
    xs = list(map(int, inp.split()))[1::2]
    pos = sum(x > 0 for x in xs)
    return "Yes" if min(pos, len(xs) - pos) <= 1 else "No"


def gen(rng):
    n = rng.choice([2, 3, rng.randint(2, 100), rng.randint(2, 3000)])
    neg = rng.choice([0, 1, 2, rng.randint(0, n)])
    pts = set()
    while len(pts) < n:
        x = rng.randint(1, rng.choice([1, 10 ** 9])) * (-1 if len(pts) < neg else 1)
        pts.add((x, rng.randint(-10 ** 9, 10 ** 9)))
    pts = list(pts); rng.shuffle(pts)
    return f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts)


def extra():
    return [("boundary", "two points opposite sides", "2\n1 0\n-1 0\n"), ("adversarial", "two on each side", "4\n1 1\n2 2\n-1 1\n-2 2\n"),
            ("maxSize", "n=10^5 one negative", "100000\n-1000000000 0\n" + "".join(f"1000000000 {i - 50000}\n" for i in range(99999)))]
