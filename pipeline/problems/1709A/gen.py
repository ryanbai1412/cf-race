import itertools
import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def all_cases():
    """All 18 valid inputs: 1,2,3 appear exactly once among x,a,b,c."""
    cases = []
    for x in (1, 2, 3):
        rest = [k for k in (1, 2, 3) if k != x]
        for doors in itertools.permutations(range(3), 2):
            abc = [0, 0, 0]
            abc[doors[0]] = rest[0]
            abc[doors[1]] = rest[1]
            cases.append(f"{x}\n{abc[0]} {abc[1]} {abc[2]}")
    return cases


def main(outdir):
    rnd = random.Random(1709)
    w = Writer(outdir)
    cases = all_cases()
    # every possible input in one max test (t=18)
    w.add(multi(cases))
    # single-case tests
    for c in cases[:4]:
        w.add(multi([c]))
    # random shuffles
    for _ in range(5):
        cs = cases[:]
        rnd.shuffle(cs)
        w.add(multi(cs[:rnd.randint(1, 18)]))


if __name__ == "__main__":
    main(sys.argv[1])
