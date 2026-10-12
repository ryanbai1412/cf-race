from rlib import *

CONSTRAINTS = "n in 1..100; a_i in 0..100; m in 0..100; shots x in 1..n, 1 <= y <= current birds on wire x."
UNIQUENESS = "Unique simulation output."
STATEMENT = "Reviewed full statement: left birds go up (y-1), right birds go down (a-y), boundary birds fly away."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    a = ls[1].split(" ")
    need(len(a) == n, "n wires")
    a = nums(a, 0, 100)
    m = num(ls[2], 0, 100)
    need(len(ls) == m + 3, "m shots")
    for l in ls[3:]:
        p = l.split(" ")
        need(len(p) == 2, "x y")
        x = num(p[0], 1, n) - 1
        y = num(p[1], 1, 10 ** 9)
        need(y <= a[x], "bird exists")
        if x > 0: a[x - 1] += y - 1
        if x < n - 1: a[x + 1] += a[x] - y
        a[x] = 0


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]; a = t[1:n + 1]; m = t[n + 1]; q = t[n + 2:]
    for i in range(m):
        x, y = q[2 * i] - 1, q[2 * i + 1]
        left, right = y - 1, a[x] - y
        a[x] = 0
        if x: a[x - 1] += left
        if x + 1 < n: a[x + 1] += right
    return "\n".join(map(str, a))


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), 100])
    a = [rng.randint(0, 100) for _ in range(n)]
    shots, b = [], a[:]
    for _ in range(rng.choice([0, rng.randint(0, 100), 100])):
        live = [i for i in range(n) if b[i] > 0]
        if not live:
            break
        x = rng.choice(live); y = rng.randint(1, b[x])
        if x: b[x - 1] += y - 1
        if x + 1 < n: b[x + 1] += b[x] - y
        b[x] = 0
        shots.append(f"{x + 1} {y}")
    return f"{n}\n{joined(a)}\n{len(shots)}\n" + "".join(s + "\n" for s in shots)


def extra():
    return [("boundary", "no shots", "1\n0\n0\n"), ("adversarial", "edge wires lose birds", "2\n3 3\n2\n1 2\n2 1\n"),
            ("maxSize", "100 wires 100 shots", "100\n" + joined([100] * 100) + "\n100\n" + "".join(f"{i + 1} 1\n" for i in range(100)))]
