import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]


from math import gcd

CHECKER = "Single integer count of triples 1<=a<=b<=c<=n; unique, exact token comparison."
STATEMENT = "Legend defines right triangles with integer sides a<=b<=c<=n, input (1<=n<=1e4), output present."


def solve(s):
    n = int(s)
    count = 0
    p = 2
    while p * p + 1 <= n:
        for q in range(1 + p % 2, p, 2):
            if gcd(p, q) == 1:
                count += n // (p * p + q * q)
        p += 1
    return f"{count}\n"


def cases(g):
    out = [("boundary", "n=1", fmt(1)), ("boundary", "n=4 (answer 0)", fmt(4)), ("boundary", "n=5 first triple", fmt(5)),
           ("adversarial", "n=25 (two distinct triples with c=25)", fmt(25)), ("adversarial", "n=65 (four triples with c=65)", fmt(65)),
           ("adversarial", "n=9999", fmt(9999)), ("maxSize", "n=10000 maximum", fmt(10000)), ("maxSize", "n=9997", fmt(9997))]
    out += [("random", "random n", fmt(n)) for n in g.sample(range(1, 10001), 110)]
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
