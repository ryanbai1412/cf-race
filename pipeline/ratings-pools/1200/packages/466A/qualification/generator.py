import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single minimum integer cost; unique value, exact token comparison."
STATEMENT = "Full legend, input (n,m,a,b in [1,1000]), output and note present in the pinned source row."


def solve(s):
    n, m, a, b = ints(s)
    return str(min(n * a, n // m * b + min(n % m * a, b))) + "\n"


def cases(g):
    out = [
        ("boundary", "all parameters minimal (1 1 1 1)", fmt([1, 1, 1, 1])),
        ("boundary", "m > n: one m-ticket cheaper than n singles", fmt([3, 1000, 1000, 1])),
        ("boundary", "n == m", fmt([7, 7, 3, 20])),
        ("adversarial", "remainder cheaper as an extra m-ticket than singles", fmt([1000, 999, 1000, 2])),
        ("adversarial", "m-ticket never worth it (b >= m*a)", fmt([1000, 7, 1, 1000])),
        ("adversarial", "tie b == m*a", fmt([10, 3, 2, 6])),
        ("maxSize", "all parameters maximal", fmt([1000, 1000, 1000, 1000])),
        ("maxSize", "n maximal, singles maximal, cheap m=1 ticket", fmt([1000, 1, 1000, 1])),
    ]
    out += fill(g, lambda g: fmt([g.randint(1, 1000) for _ in range(4)]), 60)
    out += fill(g, lambda g: fmt([g.randint(1, 30) for _ in range(4)]), 60, reason="small random")
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
