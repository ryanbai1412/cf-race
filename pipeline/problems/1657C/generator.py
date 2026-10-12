import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "t lines of two integers; unique, exact token comparison."
STATEMENT = "Legend (remove shortest good prefix: regular or palindrome length>=2), input (1<=t<=1e4, sum n<=5e5), output present."


def one(s):
    i, n, ops = 0, len(s), 0
    while i + 1 < n:
        if s[i] == "(":
            i += 2
        else:
            j = s.find(")", i + 1)
            if j < 0:
                break
            i = j + 1
        ops += 1
    return ops, n - i


def solve(s):
    t = s.split()
    return "".join("%d %d\n" % one(t[2 + 2 * k]) for k in range(int(t[0])))


def br(g, n):
    return "".join(g.choice("()") for _ in range(n))


def multi(*strs):
    return fmt(len(strs), *[x for s in strs for x in (len(s), s)])


def cases(g):
    out = [("boundary", "single char", multi("(", ")")), ("boundary", "t=1 n=2", multi("))")),
           ("adversarial", "')' then long run of '(' with no closing", multi(")" + "(" * 20)),
           ("adversarial", "palindrome vs regular choice", multi(")(()", "(()())", ")((((()")),
           ("maxSize", "n=5e5 single random", multi(br(g, 500000))), ("maxSize", "n=5e5 ')' + '(' * (n-1)", multi(")" + "(" * 499999)),
           ("maxSize", "t=1e4, n=50 each", multi(*[br(g, 50) for _ in range(10000)])),
           ("maxSize", "n=5e5 alternating ')(' worst scan", multi(")(" * 250000))]
    out += fill(g, lambda g: multi(*[br(g, g.randint(1, 8)) for _ in range(g.randint(1, 5))]), 80, reason="small random")
    out += fill(g, lambda g: multi(*[br(g, g.randint(1, 2000)) for _ in range(g.randint(1, 10))]), 30)
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
