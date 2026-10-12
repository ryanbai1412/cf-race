import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Deterministic formatted string; unique, exact token comparison (no spaces in output)."
STATEMENT = "Legend gives every formatting rule; input notation rules and output present in the pinned source row."


def solve(s):
    t = s.split()[0]
    neg = t.startswith("-")
    t = t.lstrip("-")
    ip, _, fp = t.partition(".")
    fp = (fp + "00")[:2]
    groups = []
    while len(ip) > 3:
        groups.insert(0, ip[-3:])
        ip = ip[:-3]
    body = "$" + ",".join([ip] + groups) + "." + fp
    return (f"({body})" if neg else body) + "\n"


def number(g, ilen, flen, neg):
    ip = "0" if ilen == 0 else str(g.randint(1, 9)) + "".join(str(g.randint(0, 9)) for _ in range(ilen - 1))
    fp = "".join(str(g.randint(0, 9)) for _ in range(flen))
    t = ip + ("." + fp if flen else "")
    zero = set(t) <= set("0.")
    return ("-" if neg and not zero else "") + t


def rand(g):
    ilen = g.randint(0, 40)
    flen = g.choice([0, 0, 1, 2, 3, g.randint(1, 40)])
    return fmt(number(g, ilen, flen, g.random() < 0.5))


def cases(g):
    out = [("boundary", "single zero", fmt("0")), ("boundary", "single digit", fmt("7")),
           ("boundary", "zero with many fractional zeros", fmt("0.000")),
           ("boundary", "three-digit integer part (no comma)", fmt("999")),
           ("boundary", "four-digit integer part (one comma)", fmt("1000")),
           ("adversarial", "negative number that truncates to zero", fmt("-0.001")),
           ("adversarial", "fraction truncated not rounded", fmt("-12345678.999")),
           ("adversarial", "one fractional digit padded", fmt("-0.5")),
           ("adversarial", "six-digit integer exact groups", fmt("-123456")),
           ("maxSize", "100 characters: minus, 98-digit integer part", fmt("-" + number(g, 99, 0, False))),
           ("maxSize", "100 characters: 0 point 98 digits", fmt("0." + "9" * 98)),
           ("maxSize", "100 characters: negative long integer and fraction", fmt(number(g, 50, 48, True)))]
    out += fill(g, rand, 110)
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
