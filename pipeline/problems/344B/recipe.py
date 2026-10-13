from genlib import *  # noqa: F401,F403

CHECKER = "Three bond counts or Impossible; the linear system x+z=a, x+y=b, y+z=c has at most one solution, so exact token comparison is sound despite 'output any'."
STATEMENT = "Legend (three atoms with valences, bonds between pairs), input (1<=a,b,c<=1e6), output present."


def solve(s):
    a, b, c = ints(s)
    t = a + b + c
    x, y, z = (a + b - c), (b + c - a), (c + a - b)
    if t % 2 or min(x, y, z) < 0:
        return "Impossible\n"
    return f"{x // 2} {y // 2} {z // 2}\n"


def cases(g):
    E = 10 ** 6
    out = [("boundary", "all ones (odd sum)", fmt([1, 1, 1])), ("boundary", "1 1 2", fmt([1, 1, 2])), ("boundary", "all max", fmt([E, E, E])),
           ("adversarial", "triangle equality zero bond", fmt([3, 5, 2])), ("adversarial", "triangle violated", fmt([1, 1, 4])),
           ("adversarial", "even sum but negative", fmt([1, 1, 10 ** 6])), ("maxSize", "max one atom", fmt([E, E, 2]))]
    out += fill(g, lambda g: fmt([g.randint(1, 8) for _ in range(3)]), 90, reason="small random")
    out += fill(g, lambda g: fmt([g.randint(1, E) for _ in range(3)]), 25)
    out += fill(g, lambda g: fmt([(p := g.randint(0, E // 2)) + (q := g.randint(0, E // 2)), q + (r := g.randint(1, E // 2)), r + p]), 15, reason="constructed feasible")
    return [c for c in out if min(ints(c[2])) >= 1]
