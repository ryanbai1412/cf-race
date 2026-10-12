import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Sequence of integers, one per type-3 query; unique, exact token comparison."
STATEMENT = "Legend defines 3 operation types, input (1<=n,m<=1e5, values per type), output present."


def solve(s):
    lines = s.split("\n")
    n, m = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    add, out = 0, []
    for line in lines[2:2 + m]:
        op = list(map(int, line.split()))
        if op[0] == 1:
            a[op[1] - 1] = op[2] - add
        elif op[0] == 2:
            add += op[1]
        else:
            out.append(a[op[1] - 1] + add)
    return "".join(f"{x}\n" for x in out)


def make(g, n, m, big=10 ** 9, weights=(1, 1, 1)):
    a = [g.randint(1, big) for _ in range(n)]
    ops = []
    for _ in range(m):
        t = g.choices((1, 2, 3), weights)[0]
        ops.append([1, g.randint(1, n), g.randint(1, big)] if t == 1 else [2, g.randint(1, 10 ** 4)] if t == 2 else [3, g.randint(1, n)])
    if not any(o[0] == 3 for o in ops):
        ops[-1] = [3, g.randint(1, n)]
    return fmt([n, m], a, *ops)


def cases(g):
    out = [("boundary", "n=m=1 single query", fmt([1, 1], [1], [3, 1])),
           ("adversarial", "assignment after increments must not get earlier increments", fmt([1, 4], [5], [2, 3], [1, 1, 7], [2, 1], [3, 1])),
           ("adversarial", "values exceed 32 bits after many increments", make(g, 1, 100000, 10 ** 9, (0, 9, 1))),
           ("maxSize", "n=m=1e5 mixed operations", make(g, 100000, 100000)),
           ("maxSize", "n=m=1e5 mostly queries", make(g, 100000, 100000, weights=(1, 1, 8))),
           ("boundary", "max values a=1e9, x=1e9", fmt([2, 3], [10 ** 9, 10 ** 9], [1, 2, 10 ** 9], [2, 10 ** 4], [3, 2]))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), g.randint(1, 20), 100), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 1000), g.randint(1, 1000)), 30, reason="medium random")
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
