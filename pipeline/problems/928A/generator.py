import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Yes/No; unique, exact token comparison."
STATEMENT = "Legend (case-insensitive, O/0 and 1/l/I equivalent), input (|s|<=50, 1<=n<=1000, existing logins pairwise non-similar), output present."
AL = "abcoOilIL01_Z9"


def norm(s):
    return s.lower().replace("o", "0").replace("l", "1").replace("i", "1")


def solve(t):
    v = t.split()
    s, n = norm(v[0]), int(v[1])
    return "No\n" if any(norm(x) == s for x in v[2:2 + n]) else "Yes\n"


def word(g, n):
    return "".join(g.choice(AL) for _ in range(n))


def make(g, n, length):
    seen, logs = set(), []
    while len(logs) < n:
        w = word(g, g.randint(1, length))
        if norm(w) not in seen:
            seen.add(norm(w))
            logs.append(w)
    s = word(g, g.randint(1, length)) if g.random() < 0.5 else "".join(
        {"o": "0", "0": "O", "l": "I", "1": "l", "i": "L"}.get(c, c.swapcase()) for c in g.choice(logs))
    return fmt(s, n, *logs)


def cases(g):
    out = [("boundary", "single char", fmt("a", 1, "A")), ("boundary", "underscore", fmt("_", 1, "a")),
           ("adversarial", "o vs 0", fmt("0", 1, "o")), ("adversarial", "1 vs I vs l", fmt("1", 2, "x", "I")), ("adversarial", "i vs L", fmt("i", 1, "L")),
           ("adversarial", "0 is not 1", fmt("0", 1, "1")), ("maxSize", "n=1000 length 50", make(g, 1000, 50))]
    out += fill(g, lambda g: make(g, g.randint(1, 5), 3), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(6, 1000), 50), 25)
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
