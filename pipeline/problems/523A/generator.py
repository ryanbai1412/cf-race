import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



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


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
