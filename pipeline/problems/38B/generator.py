import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend, input (two distinct squares, rook and knight not attacking each other), output present."
K = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]


def sq(t):
    return ord(t[0]) - 97, int(t[1]) - 1


def knight(a, b):
    return (abs(a[0] - b[0]), abs(a[1] - b[1])) in ((1, 2), (2, 1))


def valid(r, k):
    return r != k and r[0] != k[0] and r[1] != k[1] and not knight(r, k)


def solve(s):
    r, k = map(sq, s.split())
    return str(sum(1 for x in range(8) for y in range(8)
                   if (x, y) not in (r, k) and x != r[0] and y != r[1] and not knight((x, y), r) and not knight((x, y), k))) + "\n"


def name(p):
    return chr(97 + p[0]) + str(p[1] + 1)


def cases(g):
    pairs = [(r, k) for r in [(x, y) for x in range(8) for y in range(8)] for k in [(x, y) for x in range(8) for y in range(8)] if valid(r, k)]
    out = [("boundary", "rook a1 knight b3? no: rook corner a1, knight h8", fmt(name((0, 0)), name((7, 7)))),
           ("boundary", "rook corner h8, knight corner a1", fmt(name((7, 7)), name((0, 0)))),
           ("adversarial", "knight adjacent diagonally to rook (shared knight targets)", fmt(name((3, 3)), name((4, 4)))),
           ("adversarial", "rook centre, knight edge", fmt(name((3, 4)), name((0, 7)))),
           ("maxSize", "rook in corner, knight at centre", fmt(name((0, 0)), name((3, 4)))),
           ("maxSize", "both near centre", fmt(name((4, 3)), name((2, 2))))]
    out += [("random", "random legal placement", fmt(name(r), name(k))) for r, k in g.sample(pairs, 150)]
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
