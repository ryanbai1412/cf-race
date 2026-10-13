import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Winner name Ciel/Hanako; unique, exact token comparison."
STATEMENT = "Legend with turn rules, input (0<=x,y<=1e6), output present in the pinned source row."


def solve(s):
    x, y = ints(s)
    turn = 0
    while True:
        order = ((2, 2), (1, 12), (0, 22)) if turn == 0 else ((0, 22), (1, 12), (2, 2))
        for a, b in order:
            if x >= a and y >= b:
                x, y = x - a, y - b
                break
        else:
            return ("Hanako" if turn == 0 else "Ciel") + "\n"
        turn ^= 1


def cases(g):
    out = [("boundary", "empty pile", fmt(0, 0)), ("boundary", "x=0 y=21 cannot move", fmt(0, 21)),
           ("boundary", "x=0 y=22 one move", fmt(0, 22)), ("boundary", "x=2 y=2 one move", fmt(2, 2)),
           ("adversarial", "only 100s, y=1", fmt(10 ** 6, 1)), ("adversarial", "x=1 y=12 then 0", fmt(1, 12)),
           ("adversarial", "only 10s large", fmt(0, 10 ** 6)), ("adversarial", "only 100s large", fmt(10 ** 6, 0)),
           ("maxSize", "x=y=1e6", fmt(10 ** 6, 10 ** 6)), ("maxSize", "x=1e6 y=999999", fmt(10 ** 6, 999999))]
    out += fill(g, lambda g: fmt(g.randint(0, 30), g.randint(0, 300)), 70, reason="small random")
    out += fill(g, lambda g: fmt(g.randint(0, 10 ** 4), g.randint(0, 10 ** 4)), 30)
    out += fill(g, lambda g: fmt(g.randint(0, 10 ** 6), g.randint(0, 10 ** 6)), 3, reason="large random")
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
