from rlib import *

CONSTRAINTS = "t in 1..3000; each case x, y in 0..50."
UNIQUENESS = "Unique integer per case."
STATEMENT = "Reviewed full statement: 0 at origin, 1 if x^2+y^2 is a perfect square, else 2."


def validate(inp):
    ls = lines(inp)
    t = num(ls[0], 1, 3000)
    need(len(ls) == t + 1, "t cases")
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 2, "x y")
        num(p[0], 0, 50); num(p[1], 0, 50)


def solve(inp):
    v = list(map(int, inp.split()))[1:]
    out = []
    for i in range(0, len(v), 2):
        d = v[i] ** 2 + v[i + 1] ** 2
        out.append("0" if d == 0 else "1" if any(k * k == d for k in range(72)) else "2")
    return "\n".join(out)


def gen(rng):
    t = rng.choice([1, rng.randint(1, 100), rng.randint(1, 3000)])
    return f"{t}\n" + "".join(f"{rng.randint(0, 50)} {rng.randint(0, 50)}\n" for _ in range(t))


def extra():
    return [("boundary", "origin", "1\n0 0\n"), ("adversarial", "axis points and 3-4-5", "4\n0 7\n3 4\n1 1\n50 50\n"),
            ("maxSize", "t=3000 full grid sweep", "3000\n" + "".join(f"{i % 51} {i // 51 % 51}\n" for i in range(3000)))]
