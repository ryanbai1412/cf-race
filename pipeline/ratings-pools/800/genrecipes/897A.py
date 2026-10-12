from rlib import *

CONSTRAINTS = "n, m in 1..100; s of n lowercase letters; m lines 'l r c1 c2' with 1 <= l <= r <= n."
UNIQUENESS = "Unique string."
STATEMENT = "Reviewed full statement: sequentially replace c1 by c2 in [l, r]."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n m")
    n, m = num(p[0], 1, 100), num(p[1], 1, 100)
    need(len(ls) == m + 2, "m operations")
    word(ls[1], LOWER, n, n)
    for l in ls[2:]:
        q = l.split(" ")
        need(len(q) == 4, "l r c1 c2")
        a, b = num(q[0], 1, n), num(q[1], 1, n)
        need(a <= b and len(q[2]) == 1 and len(q[3]) == 1 and q[2] in LOWER and q[3] in LOWER, "operation")


def solve(inp):
    ls = lines(inp)
    s = list(ls[1])
    for l in ls[2:]:
        a, b, c1, c2 = l.split()
        for i in range(int(a) - 1, int(b)):
            if s[i] == c1:
                s[i] = c2
    return "".join(s)


def gen(rng):
    n, m = rng.choice([1, rng.randint(1, 100), 100]), rng.choice([1, rng.randint(1, 100), 100])
    al = LOWER[:rng.randint(1, 26)]
    ops = []
    for _ in range(m):
        a = rng.randint(1, n); b = rng.randint(a, n)
        ops.append(f"{a} {b} {rng.choice(al)} {rng.choice(al)}")
    return f"{n} {m}\n" + "".join(rng.choice(al) for _ in range(n)) + "\n" + "\n".join(ops) + "\n"


def extra():
    return [("boundary", "c1 equals c2", "1 1\na\n1 1 a a\n"), ("adversarial", "chained replacement order matters", "3 2\naaa\n1 3 a b\n2 2 b c\n"),
            ("maxSize", "n=m=100", "100 100\n" + "a" * 100 + "\n" + "\n".join(f"1 100 {chr(97 + i % 26)} {chr(97 + (i + 1) % 26)}" for i in range(100)) + "\n")]
