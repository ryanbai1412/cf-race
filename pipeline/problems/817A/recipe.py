from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (moves (+-x,+-y), reach treasure), input (-1e5<=x1,y1,x2,y2<=1e5, 1<=x,y<=1e5), output present."


def solve(s):
    x1, y1, x2, y2, x, y = ints(s)
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    if dx % x or dy % y or (dx // x) % 2 != (dy // y) % 2:
        return "NO\n"
    return "YES\n"


def make(g, r, step):
    return fmt([g.randint(-r, r) for _ in range(4)], [g.randint(1, step), g.randint(1, step)])


def cases(g):
    E = 10 ** 5
    out = [("boundary", "same point", fmt([0, 0, 0, 0], [E, E])), ("boundary", "extremes step 1", fmt([-E, -E, E, E], [1, 1])),
           ("adversarial", "parity mismatch", fmt([0, 0, 0, 6], [2, 3])), ("adversarial", "dx zero odd dy steps", fmt([0, 0, 0, 3], [1, 3])),
           ("adversarial", "parity match", fmt([0, 0, 4, 6], [2, 3])), ("maxSize", "max coords step 2e5 span", fmt([-E, E, E, -E], [E, E]))]
    out += fill(g, lambda g: make(g, 6, 3), 90, reason="small random")
    out += fill(g, lambda g: make(g, E, E), 25)
    return out
