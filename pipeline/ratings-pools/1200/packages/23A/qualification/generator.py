import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer length; unique, exact token comparison."
STATEMENT = "Legend, input (one lowercase string, 1..100 chars), output present in the pinned source row."


def solve(s):
    t = s.split()[0]
    for length in range(len(t) - 1, 0, -1):
        seen = set()
        for i in range(len(t) - length + 1):
            w = t[i:i + length]
            if w in seen:
                return f"{length}\n"
            seen.add(w)
    return "0\n"


def word(g, n, alpha):
    return "".join(g.choice(alpha) for _ in range(n))


def cases(g):
    out = [("boundary", "single character", fmt("a")), ("boundary", "two equal characters", fmt("zz")),
           ("boundary", "all distinct letters (answer 0)", fmt("abcdefghijklmnopqrstuvwxyz")),
           ("adversarial", "overlapping occurrences ababa...", fmt("ab" * 50)),
           ("adversarial", "repeat at both ends only", fmt("xyz" + "abcdefghijklmnopqrstuvw" + "xyz")),
           ("maxSize", "100 identical letters (answer 99)", fmt("a" * 100)),
           ("maxSize", "length 100 random over 2 letters", fmt(word(g, 100, "ab"))),
           ("maxSize", "length 100 random over 26 letters", fmt(word(g, 100, "abcdefghijklmnopqrstuvwxyz")))]
    for alpha in ("ab", "abc", "abcdefghijklmnopqrstuvwxyz"):
        out += fill(g, lambda g, a=alpha: fmt(word(g, g.randint(1, 100), a)), 30)
    out += fill(g, lambda g: fmt(word(g, g.randint(1, 8), "ab")), 30, reason="tiny binary strings")
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
