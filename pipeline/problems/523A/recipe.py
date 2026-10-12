from genlib import *  # noqa: F401,F403

CHECKER = "Fixed 2w lines of 2h characters; unique, exact token comparison."
STATEMENT = "Legend (rotate 90 clockwise, flip horizontally, zoom x2), input (1<=w,h<=100, '.'/'*' pixels), output present."


def solve(s):
    t = s.split()
    w, h = int(t[0]), int(t[1])
    img = t[2:2 + h]
    rows = []
    for j in range(w):
        line = "".join(img[i][j] * 2 for i in range(h))
        rows += [line, line]
    return "".join(r + "\n" for r in rows)


def make(g, w, h, p=0.5):
    return fmt([w, h], *["".join("*" if g.random() < p else "." for _ in range(w)) for _ in range(h)])


def cases(g):
    out = [("boundary", "1x1 dot", fmt([1, 1], ".")), ("boundary", "1x1 star", fmt([1, 1], "*")),
           ("adversarial", "asymmetric 2x3 (detects wrong rotation/flip)", fmt([2, 3], "*.", "..", ".*")),
           ("maxSize", "100x100 random", make(g, 100, 100)), ("maxSize", "w=100 h=1", make(g, 100, 1)), ("maxSize", "w=1 h=100", make(g, 1, 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 5), g.randint(1, 5), g.random()), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100), g.random()), 30)
    return out
