from genlib import *  # noqa: F401,F403

CHECKER = "Single integer or -1; unique, exact token comparison."
STATEMENT = "Legend (arithmetic scream times, first common), input (1<=a,b,c,d<=100), output present."


def solve(s):
    a, b, c, d = ints(s)
    for t in range(max(b, d), 30000):
        if (t - b) % a == 0 and (t - d) % c == 0:
            return f"{t}\n"
    return "-1\n"


def cases(g):
    out = [("boundary", "all ones", fmt([1, 1], [1, 1])), ("boundary", "all 100", fmt([100, 100], [100, 100])),
           ("adversarial", "never (parity)", fmt([2, 1], [2, 2])), ("adversarial", "large lcm 99 100", fmt([99, 100], [100, 1])), ("adversarial", "sample", fmt([20, 2], [9, 19])),
           ("maxSize", "coprime max offsets", fmt([97, 100], [89, 1]))]
    out += fill(g, lambda g: fmt([g.randint(1, 100), g.randint(1, 100)], [g.randint(1, 100), g.randint(1, 100)]), 80)
    out += fill(g, lambda g: fmt([2 * g.randint(1, 50), g.randint(1, 100)], [2 * g.randint(1, 50), g.randint(1, 100)]), 30, reason="even steps (often -1)")
    return out
