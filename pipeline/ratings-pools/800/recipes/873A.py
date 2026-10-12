from rlib import *

CONSTRAINTS = "1 <= k <= n <= 100, x in 1..99; n sorted a_i in 2..100 with x < min a."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: replace the k largest chores with x."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100); num(t[1], 1, n); x = num(t[2], 1, 99)
    need(len(t) == n + 3, "n values")
    a = nums(t[3:], 2, 100)
    need(all(a[i] <= a[i + 1] for i in range(n - 1)) and x < min(a), "sorted and x < min")


def solve(inp):
    t = list(map(int, inp.split()))
    n, k, x, a = t[0], t[1], t[2], t[3:]
    return str(sum(a[:n - k]) + k * x)


def extra():
    return [("boundary", "n=k=1", "1 1 1\n2\n"), ("adversarial", "k=n all replaced", "3 3 5\n6 7 8\n"),
            ("maxSize", "n=100 k=1 all 100", "100 1 99\n" + joined([100] * 100) + "\n"),
            ("maxSize", "n=100 k=50 increasing", "100 50 1\n" + joined(sorted(2 + i % 99 for i in range(100))) + "\n")]
