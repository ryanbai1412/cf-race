import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



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


def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
