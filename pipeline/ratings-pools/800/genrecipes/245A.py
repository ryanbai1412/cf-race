from rlib import *

CONSTRAINTS = "n in 2..1000; t in {1,2}; x,y >= 0 with x+y = 10; at least one command per server."
UNIQUENESS = "Two fixed LIVE/DEAD lines."
STATEMENT = "Reviewed full statement: alive iff successes >= half of the packets sent to that server."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 2, 1000)
    need(len(ls) == n + 1, "n commands")
    seen = set()
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 3, "t x y")
        t, x, y = num(p[0], 1, 2), num(p[1], 0, 10), num(p[2], 0, 10)
        need(x + y == 10, "x+y=10")
        seen.add(t)
    need(seen == {1, 2}, "both servers pinged")


def solve(inp):
    t = list(map(int, inp.split()))[1:]
    ok, sent = [0, 0, 0], [0, 0, 0]
    for i in range(0, len(t), 3):
        ok[t[i]] += t[i + 1]; sent[t[i]] += 10
    return "\n".join("LIVE" if 2 * ok[s] >= sent[s] else "DEAD" for s in (1, 2))


def gen(rng):
    n = rng.choice([2, 3, rng.randint(2, 1000), 1000])
    ts = [1, 2] + [rng.randint(1, 2) for _ in range(n - 2)]
    rng.shuffle(ts)
    bias = rng.choice([0, 4, 5, 6, 10])
    xs = [min(10, max(0, bias + rng.randint(-2, 2))) for _ in range(n)]
    return f"{n}\n" + "\n".join(f"{t} {x} {10 - x}" for t, x in zip(ts, xs)) + "\n"


def extra():
    return [("boundary", "exactly half on both", "2\n1 5 5\n2 5 5\n"), ("boundary", "all lost", "2\n1 0 10\n2 0 10\n"),
            ("adversarial", "one short of half after aggregation", "3\n1 10 0\n1 0 10\n2 4 6\n"),
            ("maxSize", "n=1000 alternating", "1000\n" + "".join(f"{1 + i % 2} {i % 11} {10 - i % 11}\n" for i in range(1000)))]
