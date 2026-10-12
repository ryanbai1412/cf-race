from rlib import *

CONSTRAINTS = "n in 2..3*10^4; distinct digit strings of equal length 1..20."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: longest common prefix length."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 2, 30000)
    need(len(ls) == n + 1, "n strings")
    L = len(ls[1])
    for s in ls[1:]:
        word(s, DIGITS, L, L)
    need(1 <= L <= 20 and len(set(ls[1:])) == n, "distinct, length 1..20")


def solve(inp):
    ss = lines(inp)[1:]
    a, b = min(ss), max(ss)
    k = 0
    while k < len(a) and a[k] == b[k]:
        k += 1
    return str(k)


def gen(rng):
    L = rng.choice([1, 2, rng.randint(1, 20), 20])
    p = rng.randint(0, L - 1)
    cap = 10 ** (L - p) - 10 ** (L - p - 1) * 0
    n = min(rng.choice([2, 3, rng.randint(2, 50), rng.randint(2, 2000)]), cap, 30000)
    if n < 2:
        n = 2
        p = L - 1
    pre = "".join(rng.choice(DIGITS) for _ in range(p))
    out = set()
    while len(out) < n:
        out.add(pre + "".join(rng.choice(DIGITS) for _ in range(L - p)))
    return f"{n}\n" + "\n".join(sorted(out, key=lambda _: rng.random())) + "\n"


def extra():
    return [("boundary", "n=2 length 1", "2\n0\n9\n"), ("boundary", "prefix of length 19", "2\n12345678901234567890\n12345678901234567891\n"),
            ("adversarial", "first and last share prefix, middle breaks it", "3\n1234\n1299\n1235\n"),
            ("maxSize", "n=30000 length 20 sharing 15 digits", "30000\n" + "\n".join(f"555554444433333{i:05d}" for i in range(30000)) + "\n")]
