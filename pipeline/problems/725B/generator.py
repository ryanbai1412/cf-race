import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer (up to ~6e18, 64-bit); unique, exact token comparison."
STATEMENT = "Legend (two attendants serving rows 1&3, 2&4, then 5&7 ... in seat order f e d a b c), input ('ns', 1<=n<=1e18), output present."
ORDER = {"f": 1, "e": 2, "d": 3, "a": 4, "b": 5, "c": 6}


def solve(s):
    t = s.split()[0]
    return f"{wait(int(t[:-1]), t[-1])}\n"


def wait(n, seat):
    k = (n - 1) // 4
    pos = (n - 1) % 4
    t = k * 16
    if pos in (1, 3):
        t += 7
    return t + ORDER[seat]


def cases(g):
    E = 10 ** 18
    out = [("boundary", "1f", fmt("1f")), ("boundary", "1c", fmt("1c")), ("boundary", "1e18 c", fmt(f"{E}c")),
           ("adversarial", "rows 1..8 all seats", fmt("8a")), ("adversarial", "row 3 (served with 1)", fmt("3d")),
           ("maxSize", "1e18-1 f", fmt(f"{E - 1}f")), ("maxSize", "1e18-2 a", fmt(f"{E - 2}a"))]
    out += [("random", "rows 1..20 every seat", fmt(f"{r}{c}")) for r in range(1, 21) for c in "abcdef"]
    out += fill(g, lambda g: fmt(f"{g.randint(1, E)}{g.choice('abcdef')}"), 30)
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
