from genlib import *  # noqa: F401,F403

CHECKER = "Single integer; unique, exact token comparison."
STATEMENT = "Legend (seating rules one-seater, two-seater, half-occupied), input (1<=n,a,b<=2e5, ti in {1,2}), output present."


def solve(s):
    v = ints(s)
    n, a, b = v[0], v[1], v[2]
    half, denied = 0, 0
    for t in v[3:3 + n]:
        if t == 1:
            if a:
                a -= 1
            elif b:
                b -= 1
                half += 1
            elif half:
                half -= 1
            else:
                denied += 1
        elif b:
            b -= 1
        else:
            denied += 2
    return f"{denied}\n"


def make(g, n, a, b, p=0.5):
    return fmt([n, a, b], [1 if g.random() < p else 2 for _ in range(n)])


def cases(g):
    N = 2 * 10 ** 5
    out = [("boundary", "n=1 pair", fmt([1, 1, 1], [2])), ("boundary", "n=1 single", fmt([1, 1, 1], [1])),
           ("adversarial", "singles fill half tables", fmt([5, 1, 1], [1, 1, 1, 1, 2])), ("adversarial", "pair after half table used", fmt([3, 1, 1], [1, 1, 2])),
           ("maxSize", "n=2e5 all pairs b=1", fmt([N, 1, 1], [2] * N)), ("maxSize", "n=2e5 all singles", fmt([N, N, N], [1] * N)), ("maxSize", "n=2e5 random", make(g, N, 1000, 1000))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(1, 3), g.randint(1, 3), g.random()), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(9, 3000), g.randint(1, 1000), g.randint(1, 1000), g.random()), 25)
    return out
