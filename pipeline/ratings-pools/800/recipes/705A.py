from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 100."
UNIQUENESS = "Sentence is fully determined."
STATEMENT = "Reviewed full statement: alternate 'I hate'/'I love' joined by ' that ', ending ' it'."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 100)


def solve(inp):
    n = int(inp.split()[0])
    return " that ".join("I hate" if i % 2 == 0 else "I love" for i in range(n)) + " it"


def extra():
    return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("maxSize", "n=100", "100\n"), ("adversarial", "n=99 odd ends with hate", "99\n")]
