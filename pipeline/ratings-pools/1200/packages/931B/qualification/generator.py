import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Round number or Final!; unique, exact token comparison."
STATEMENT = "Legend (play-off by sorted ids), input (2<=n<=256 power of two, 1<=a,b<=n, a!=b), output present."


def solve(s):
    n, a, b = ints(s)
    a, b, r = a - 1, b - 1, 0
    while a != b:
        a, b, r = a >> 1, b >> 1, r + 1
    return "Final!\n" if (1 << r) == n else f"{r}\n"


def cases(g):
    out = [("boundary", "n=2", fmt([2, 1, 2])), ("boundary", "n=256 final", fmt([256, 1, 256])), ("boundary", "n=256 round 1", fmt([256, 255, 256])),
           ("adversarial", "n=4 1 3 final", fmt([4, 3, 1])), ("adversarial", "n=8 4 5 final", fmt([8, 4, 5])), ("maxSize", "n=256 128 129", fmt([256, 128, 129]))]
    out += [("random", "n=8 all pairs", fmt([8, a, b])) for a in range(1, 9) for b in range(1, 9) if a != b and (a + b) % 2 == 1]
    out += fill(g, lambda g: fmt([(n := 2 ** g.randint(4, 8)), *g.sample(range(1, n + 1), 2)]), 90)
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
