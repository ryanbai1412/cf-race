from rlib import *

CONSTRAINTS = "n, m in 3..50, n odd."
UNIQUENESS = "The drawing is fully determined."
STATEMENT = "Reviewed full statement and samples: even rows full '#', odd rows single '#' alternating right/left."


def validate(inp):
    n, m = nums(exact_tokens(inp, 2), 3, 50)
    need(n % 2 == 1, "n odd")


def solve(inp):
    n, m = map(int, inp.split())
    out = []
    for i in range(n):
        if i % 2 == 0:
            out.append("#" * m)
        elif i % 4 == 1:
            out.append("." * (m - 1) + "#")
        else:
            out.append("#" + "." * (m - 1))
    return "\n".join(out)


def extra():
    return [("boundary", "minimum 3x3", "3 3\n"), ("adversarial", "n=5 shows left turn", "5 3\n"),
            ("maxSize", "49x50", "49 50\n"), ("maxSize", "n=7 m=50", "7 50\n")]
