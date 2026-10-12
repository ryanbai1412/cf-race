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
STATEMENT = "Legend, input (1<=n<=1e9), output and note present in the pinned source row."


def solve(s):
    n = int(s)
    return str(sum(1 for k in range(1, 1 << 10) if int(bin(k)[2:]) <= n)) + "\n"


def cases(g):
    out = [("boundary", "n=1 minimum", fmt(1)), ("boundary", "n=9 just below 10", fmt(9)),
           ("boundary", "n=10 first two-digit binary number", fmt(10)), ("boundary", "n=11", fmt(11)),
           ("adversarial", "n=111111111 all ones, largest 9-digit binary", fmt(111111111)),
           ("adversarial", "n=111111110 just below all ones", fmt(111111110)),
           ("adversarial", "n=199999999 digits above 1 after leading 1", fmt(199999999)),
           ("adversarial", "n=100000000 power of ten", fmt(100000000)),
           ("adversarial", "n=101010101 alternating", fmt(101010101)),
           ("maxSize", "n=1e9 maximum (itself binary-looking)", fmt(10 ** 9)),
           ("maxSize", "n=999999999", fmt(999999999))]
    out += [("random", "binary-looking value", fmt(int(bin(k)[2:]))) for k in range(1, 512, 9)]
    out += fill(g, lambda g: fmt(g.randint(1, 10 ** 9)), 60)
    out += fill(g, lambda g: fmt(g.randint(1, 1000)), 20, reason="small random")
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
