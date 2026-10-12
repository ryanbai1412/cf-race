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
STATEMENT = "Legend (substrings containing 'bear'), input (lowercase string, 1<=|s|<=5000), output present."


def solve(s):
    t = s.split()[0]
    total, last = 0, -1
    for j in range(len(t)):
        if j >= 3 and t[j - 3:j + 1] == "bear":
            last = j - 3
        total += last + 1
    return f"{total}\n"


def word(g, n, alpha):
    out = []
    while len(out) < n:
        out.extend("bear" if g.random() < 0.15 else g.choice(alpha))
    return "".join(out[:n])


def cases(g):
    out = [("boundary", "length 1", fmt("b")), ("boundary", "exactly bear", fmt("bear")),
           ("adversarial", "near misses bea/ear", fmt("beabearbeaearbbear")), ("adversarial", "overlapping attempts", fmt("bbeearr")),
           ("maxSize", "5000 x bear repeated", fmt("bear" * 1250)), ("maxSize", "5000 no bear", fmt("z" * 5000)),
           ("maxSize", "5000 random bear-heavy", fmt(word(g, 5000, "bear")))]
    out += fill(g, lambda g: fmt(word(g, g.randint(1, 14), "bearx")), 80, reason="small random")
    out += fill(g, lambda g: fmt(word(g, g.randint(15, 5000), "abcdefghijklmnopqrstuvwxyz")), 30)
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
