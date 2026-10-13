import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]


import string

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (keep words using at most two distinct letters overall), input (1<=n<=100, total length<=1000), output present."


def solve(s):
    words = s.split()[1:]
    best = 0
    for a in string.ascii_lowercase:
        for b in string.ascii_lowercase:
            best = max(best, sum(len(w) for w in words if set(w) <= {a, b}))
    return f"{best}\n"


def make(g, n, alpha, maxlen):
    words = []
    for _ in range(n):
        letters = g.sample(alpha, min(len(alpha), g.randint(1, 3)))
        words.append("".join(g.choice(letters) for _ in range(g.randint(1, maxlen))))
    return fmt(n, *words)


def cases(g):
    out = [("boundary", "n=1 single letter", fmt(1, "a")), ("boundary", "n=1 three letters (0)", fmt(1, "abc")),
           ("adversarial", "best pair not the most frequent letters", fmt(4, "ab", "ab", "cd" * 3, "c")),
           ("maxSize", "n=100 total 1000", fmt(100, *["ab" * 5] * 100)), ("maxSize", "n=1 length 1000", fmt(1, "z" * 1000)),
           ("maxSize", "n=100 random total 1000", make(g, 100, "abcdef", 10))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), "abcd", 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), string.ascii_lowercase[:g.randint(2, 26)], 10), 30)
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
