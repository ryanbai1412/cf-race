from rlib import *

CONSTRAINTS = "odd n in 1..5, n distinct years in 2010..2100 forming a consecutive range (answer exists)."
UNIQUENESS = "Median of the consecutive range is unique."
STATEMENT = "Reviewed full statement: answer is the median year."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 5)
    need(n % 2 == 1 and len(t) == n + 1, "odd n, n years")
    a = sorted(nums(t[1:], 2010, 2100))
    need(a == list(range(a[0], a[0] + n)), "consecutive distinct years")


def solve(inp):
    t = list(map(int, inp.split()))
    return str(sorted(t[1:])[t[0] // 2])


def extra():
    return [("boundary", "n=1 min year", "1\n2010\n"), ("boundary", "n=1 max year", "1\n2100\n"),
            ("adversarial", "n=5 shuffled", "5\n2098 2100 2096 2099 2097\n"), ("maxSize", "n=5 at start", "5\n2014 2010 2012 2011 2013\n")]
