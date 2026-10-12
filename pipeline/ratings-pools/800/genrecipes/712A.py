from rlib import *

CONSTRAINTS = "n in 2..10^5; a_i in -10^9..10^9; derived b fits 32-bit (guaranteed)."
UNIQUENESS = "b_i = a_i + a_{i+1}, b_n = a_n is unique."
STATEMENT = "Reviewed full statement: recover b from alternating suffix sums a."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 2, 100000)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    a = nums(a, -10 ** 9, 10 ** 9)
    need(all(-2 ** 31 <= a[i] + a[i + 1] < 2 ** 31 for i in range(n - 1)), "b fits int32")


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    return " ".join(str(a[i] + a[i + 1]) for i in range(len(a) - 1)) + " " + str(a[-1])


def gen(rng):
    n = rng.choice([2, 3, rng.randint(2, 100), rng.randint(2, 3000)])
    b = [rng.randint(-rng.choice([1, 10, 10 ** 9]), 10 ** 9) for _ in range(n)]
    while True:
        a, s = [0] * n, 0
        for i in range(n - 1, -1, -1):
            s = b[i] - s; a[i] = s
        if all(abs(x) <= 10 ** 9 for x in a):
            return f"{n}\n{joined(a)}\n"
        b = [x // 2 for x in b]


def extra():
    return [("boundary", "n=2 zeros", "2\n0 0\n"), ("adversarial", "b exceeds 10^9 but fits int32", "2\n1000000000 1000000000\n"),
            ("maxSize", "n=10^5 extremes", "100000\n" + joined([10 ** 9, -10 ** 9] * 50000) + "\n")]
