import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "YES/NO decision; unique, exact token comparison."
STATEMENT = "Legend (axis-parallel, rotations allowed, no overlap), input (all sides 1..1000), output present."


def fits(A, B, a, b, c, d):
    for p, q in ((a, b), (b, a)):
        for r, t in ((c, d), (d, c)):
            if (p + r <= A and max(q, t) <= B) or (max(p, r) <= A and q + t <= B):
                return True
    return False


def solve(s):
    A, B, a, b, c, d = ints(s)
    return ("YES" if fits(A, B, a, b, c, d) else "NO") + "\n"


def rand(g, hi):
    return fmt([g.randint(1, hi), g.randint(1, hi)], [g.randint(1, hi), g.randint(1, hi)], [g.randint(1, hi), g.randint(1, hi)])


def cases(g):
    out = [("boundary", "all ones (NO)", fmt([1, 1], [1, 1], [1, 1])), ("boundary", "exact fit side by side", fmt([2, 1], [1, 1], [1, 1])),
           ("adversarial", "fits only with board rotated", fmt([1, 2], [1, 1], [1, 1])),
           ("adversarial", "fits only with one painting rotated", fmt([3, 2], [1, 3], [2, 1])),
           ("adversarial", "area fits but shape does not", fmt([5, 5], [3, 3], [3, 3])),
           ("maxSize", "max board, two max-height halves", fmt([1000, 1000], [500, 1000], [1000, 500])),
           ("maxSize", "max board, overflow by one", fmt([1000, 1000], [501, 1000], [500, 1000]))]
    out += fill(g, lambda g: rand(g, 1000), 50)
    out += fill(g, lambda g: rand(g, 6), 60, reason="small sides")
    out += fill(g, lambda g: rand(g, 20), 20, reason="medium sides")
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
