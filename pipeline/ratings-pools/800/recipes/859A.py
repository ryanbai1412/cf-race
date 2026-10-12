from rlib import *

CONSTRAINTS = "K in 1..25, then K distinct ranks in 1..10^6."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max(0, max rank - 25)."


def validate(inp):
    t = toks(inp)
    k = num(t[0], 1, 25)
    need(len(t) == k + 1, "K ranks")
    need(len(set(nums(t[1:], 1, 10 ** 6))) == k, "distinct")


def solve(inp):
    return str(max(0, max(map(int, inp.split()[1:])) - 25))


def extra():
    return [("boundary", "K=1 rank 1", "1\n1\n"), ("boundary", "rank exactly 25", "1\n25\n"), ("adversarial", "rank 26", "2\n26 3\n"),
            ("maxSize", "K=25 with max rank 10^6", "25\n" + joined(list(range(1, 25)) + [1000000]) + "\n")]
