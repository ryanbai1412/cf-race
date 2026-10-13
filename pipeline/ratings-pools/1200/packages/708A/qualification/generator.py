import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single string; lexicographic minimum is unique; exact token comparison."
STATEMENT = "Legend (shift exactly one non-empty substring back by one letter), input (lowercase, 1<=|s|<=1e5), output present."


def solve(s):
    t = list(s.split()[0])
    i = 0
    while i < len(t) and t[i] == "a":
        i += 1
    if i == len(t):
        t[-1] = "z"
    else:
        while i < len(t) and t[i] != "a":
            t[i] = chr(ord(t[i]) - 1)
            i += 1
    return "".join(t) + "\n"


def word(g, n, alpha="abcdefghijklmnopqrstuvwxyz"):
    return "".join(g.choice(alpha) for _ in range(n))


def cases(g):
    N = 10 ** 5
    out = [("boundary", "single a (must become z)", fmt("a")), ("boundary", "single z", fmt("z")),
           ("adversarial", "all a (last becomes z)", fmt("aaaa")), ("adversarial", "leading a then block", fmt("aabca")),
           ("maxSize", "1e5 a", fmt("a" * N)), ("maxSize", "1e5 b", fmt("b" * N)), ("maxSize", "1e5 random ab", fmt(word(g, N, "ab")))]
    out += fill(g, lambda g: fmt(word(g, g.randint(1, 8), "abz")), 100, reason="small random")
    out += fill(g, lambda g: fmt(word(g, g.randint(9, 5000))), 30)
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
