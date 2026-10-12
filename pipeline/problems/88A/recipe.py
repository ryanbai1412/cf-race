from genlib import *  # noqa: F401,F403
from itertools import combinations, permutations

CHECKER = "One of major/minor/strange; statement guarantees unambiguous classification; exact token comparison."
STATEMENT = "Legend defines notes, distances, major/minor triads; input three notes; output present."
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "B", "H"]


def solve(s):
    v = [NOTES.index(t) for t in s.split()]
    for x, y, z in permutations(v):
        d1, d2 = (y - x) % 12, (z - y) % 12
        if (d1, d2) == (4, 3):
            return "major\n"
        if (d1, d2) == (3, 4):
            return "minor\n"
    return "strange\n"


def cases(g):
    triples = []
    for c in combinations(range(12), 3):
        for p in permutations(c):
            triples.append(fmt(" ".join(NOTES[i] for i in p)))
    out = [("boundary", "C major root position", fmt("C E G")),
           ("boundary", "wraps around H->C (A minor: A C E)", fmt("E A C")),
           ("adversarial", "H major across the octave boundary", fmt("D# F# H")),
           ("adversarial", "augmented triad (strange)", fmt("C E G#")),
           ("adversarial", "diminished triad (strange)", fmt("H D F")),
           ("maxSize", "all sharps", fmt("C# F G#")), ("maxSize", "minor with sharps", fmt("G# H D#"))]
    out += [("random", "random distinct triple in random order", t) for t in g.sample(triples, 160)]
    return out
