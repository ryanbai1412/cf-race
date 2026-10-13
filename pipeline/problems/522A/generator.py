import json
import random
import sys


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"


def ints(s):
    return list(map(int, s.split()))


def fill(g, make, count, kind="random", reason="seeded random"):
    return [(kind, reason, make(g)) for _ in range(count)]



CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (case-insensitive names, valid repost order), input (1<=n<=200, names 2..24 of [A-Za-z0-9]), output present."
ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def solve(s):
    lines = s.split("\n")
    depth = {"polycarp": 1}
    for line in lines[1:1 + int(lines[0])]:
        a, _, b = line.split()
        depth[a.lower()] = depth[b.lower()] + 1
    return f"{max(depth.values())}\n"


def jumble(g, name):
    return "".join(c.upper() if g.random() < 0.5 else c.lower() for c in name)


def make(g, n, chain=0.0, maxlen=24):
    names, used = ["Polycarp"], {"polycarp"}
    rows = []
    for _ in range(n):
        while True:
            nm = "".join(g.choice(ALPHA) for _ in range(g.randint(2, maxlen)))
            if nm.lower() not in used:
                break
        used.add(nm.lower())
        parent = names[-1] if g.random() < chain else g.choice(names)
        rows.append(f"{jumble(g, nm)} reposted {jumble(g, parent)}")
        names.append(nm)
    return fmt(n, *rows)


def cases(g):
    out = [("boundary", "n=1", fmt(1, "ab reposted Polycarp")),
           ("boundary", "n=1 uppercase POLYCARP", fmt(1, "ZZ reposted POLYCARP")),
           ("adversarial", "case-variant references", fmt(3, "Ab reposted polycarp", "cD reposted aB", "EF reposted CD")),
           ("maxSize", "n=200 single chain (answer 201)", make(g, 200, 1.0)),
           ("maxSize", "n=200 random tree", make(g, 200)),
           ("maxSize", "n=200 all 24-char names", make(g, 200, 0.5, 24))]
    out += fill(g, lambda g: make(g, g.randint(1, 10), g.random(), 4), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 200), g.random()), 30)
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
