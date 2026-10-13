from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (cuts between balanced prefixes cost |ai-ai+1|, budget B), input (2<=n<=100, 1<=B<=100, 1<=ai<=100, equal evens/odds), output present."


def solve(s):
    v = ints(s)
    n, B = v[0], v[1]
    a = v[2:2 + n]
    bal, costs = 0, []
    for i in range(n - 1):
        bal += 1 if a[i] % 2 else -1
        if bal == 0:
            costs.append(abs(a[i] - a[i + 1]))
    cnt = 0
    for c in sorted(costs):
        if c <= B:
            B -= c
            cnt += 1
    return f"{cnt}\n"


def make(g, n, B, hi=100):
    half = n // 2
    a = [2 * g.randint(1, hi // 2) for _ in range(half)] + [2 * g.randint(0, (hi - 1) // 2) + 1 for _ in range(half)]
    g.shuffle(a)
    if g.random() < 0.5:
        a = []
        for _ in range(half):
            pair = [2 * g.randint(1, hi // 2), 2 * g.randint(0, (hi - 1) // 2) + 1]
            g.shuffle(pair)
            a += pair
    return fmt([len(a), B], a)


def cases(g):
    out = [("boundary", "n=2", fmt([2, 1], [1, 2])), ("boundary", "B=100 n=100 alternating", fmt([100, 100], [1 + i % 2 for i in range(100)])),
           ("adversarial", "cuts too expensive", fmt([4, 1], [1, 100, 2, 99])), ("adversarial", "no balanced prefix", fmt([4, 100], [1, 3, 2, 4])),
           ("maxSize", "n=100 random B=100", make(g, 100, 100)), ("maxSize", "n=100 B=1", make(g, 100, 1))]
    out += fill(g, lambda g: make(g, 2 * g.randint(1, 4), g.randint(1, 10), 10), 90, reason="small random")
    out += fill(g, lambda g: make(g, 2 * g.randint(5, 50), g.randint(1, 100)), 25)
    return out
