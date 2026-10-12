from genlib import *  # noqa: F401,F403
from itertools import permutations

CHECKER = "Unique permutation string or Impossible (coins pairwise distinct); exact token comparison."
STATEMENT = "Legend, input (three weighing lines X<Y / X>Y covering each pair once), output present."


def solve(s):
    rel = s.split()
    for p in permutations("ABC"):
        pos = {c: i for i, c in enumerate(p)}
        if all((pos[r[0]] < pos[r[2]]) == (r[1] == "<") for r in rel):
            return "".join(p) + "\n"
    return "Impossible\n"


def line(a, b, less, flip):
    return f"{b}{'>' if less else '<'}{a}" if flip else f"{a}{'<' if less else '>'}{b}"


def cases(g):
    pairs = [("A", "B"), ("A", "C"), ("B", "C")]
    allc = []
    for order in permutations(range(3)):
        for mask in range(8):
            for flips in range(8):
                rows = [line(*pairs[i], bool(mask >> i & 1), bool(flips >> i & 1)) for i in order]
                allc.append(fmt(*rows))
    out = [("boundary", "A<B<C sorted order", fmt("A<B", "B<C", "A<C")),
           ("boundary", "C<B<A reversed order", fmt("A>B", "B>C", "A>C")),
           ("adversarial", "cyclic A<B<C<A (Impossible)", fmt("A<B", "B<C", "C<A")),
           ("adversarial", "cyclic written with >", fmt("B>A", "C>B", "A>C")),
           ("maxSize", "middle coin varies, all >-written", fmt("C>A", "B>C", "B>A"))]
    out += [("random", "enumerated weighing set", c) for c in g.sample(allc, 150)]
    return out
