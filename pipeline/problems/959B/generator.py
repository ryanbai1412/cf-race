import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single integer (64-bit); unique, exact token comparison."
STATEMENT = "Legend (replace word by cheapest synonym), input (1<=k<=n<=1e5, 1<=m<=1e5, distinct words <=20 letters, groups partition, 1<=ai<=1e9), output present."


def solve(s):
    t = s.split()
    n, k, m = int(t[0]), int(t[1]), int(t[2])
    words = t[3:3 + n]
    cost = list(map(int, t[3 + n:3 + 2 * n]))
    i, best = 3 + 2 * n, {}
    for _ in range(k):
        x = int(t[i])
        idx = [int(y) - 1 for y in t[i + 1:i + 1 + x]]
        c = min(cost[j] for j in idx)
        for j in idx:
            best[words[j]] = c
        i += 1 + x
    return f"{sum(best[w] for w in t[i:i + m])}\n"


def make(g, n, k, m, wl=6, hi=10 ** 9):
    words = set()
    while len(words) < n:
        words.add("".join(g.choice("abcdefghij") for _ in range(g.randint(1, wl))))
    words = sorted(words)
    g.shuffle(words)
    idx = list(range(1, n + 1))
    g.shuffle(idx)
    cuts = sorted(g.sample(range(1, n), k - 1))
    groups = [idx[a:b] for a, b in zip([0] + cuts, cuts + [n])]
    return fmt([n, k, m], " ".join(words), [g.randint(1, hi) for _ in range(n)], *[[len(x)] + x for x in groups],
               " ".join(g.choice(words) for _ in range(m)))


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=k=m=1", fmt([1, 1, 1], "a", [10 ** 9], [1, 1], "a")), ("boundary", "one group all", make(g, 5, 1, 5)),
           ("adversarial", "each word own group", make(g, 6, 6, 6)),
           ("maxSize", "n=m=1e5 cost 1e9 (sum 1e14)", make(g, N, 1, N, 20, 1)), ("maxSize", "n=m=3e4 random groups", make(g, 30000, 1000, 30000, 20))]
    out += fill(g, lambda g: make(g, (n := g.randint(1, 6)), g.randint(1, n), g.randint(1, 6), 3, 20), 90, reason="small random")
    out += fill(g, lambda g: make(g, (n := g.randint(7, 2000)), g.randint(1, n), g.randint(1, 2000)), 25)
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
