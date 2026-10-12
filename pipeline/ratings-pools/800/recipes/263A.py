from rlib import *

CONSTRAINTS = "five lines of five integers in {0,1}, exactly one 1."
UNIQUENESS = "Minimum moves is a unique integer."
STATEMENT = "Reviewed full statement: Manhattan distance of the 1 to (3,3)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 5, "five lines")
    cells = []
    for l in ls:
        row = l.split(" ")
        need(len(row) == 5, "five per row")
        cells += nums(row, 0, 1)
    need(sum(cells) == 1, "exactly one 1")


def solve(inp):
    i = list(map(int, inp.split())).index(1)
    return str(abs(i // 5 - 2) + abs(i % 5 - 2))


def grid(r, c):
    return "".join(" ".join("1" if (i, j) == (r, c) else "0" for j in range(5)) + "\n" for i in range(5))


def extra():
    return [("boundary", "already centered", grid(2, 2)), ("boundary", "top-left corner", grid(0, 0)),
            ("adversarial", "edge middle", grid(4, 2)), ("maxSize", "bottom-right corner (max distance 4)", grid(4, 4)),
            ("maxSize", "top-right corner", grid(0, 4))]
