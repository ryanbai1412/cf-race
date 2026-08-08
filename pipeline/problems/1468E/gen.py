import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1468)
    w = Writer(outdir)
    # edges: all 1s, all max, mixed extremes
    w.add(multi([case([1, 1, 1, 1]), case([10000] * 4),
                 case([1, 1, 10000, 10000]), case([1, 10000, 1, 10000]),
                 case([1, 2, 3, 4]), case([4, 3, 2, 1])]))
    # all permutations of a fixed multiset
    import itertools
    w.add(multi([case(p) for p in itertools.permutations([2, 5, 7, 11])]))
    # random small
    for _ in range(2):
        w.add(multi([case([rnd.randint(1, 20) for _ in range(4)])
                     for _ in range(1000)]))
    # random full range, max t
    w.add(multi([case([rnd.randint(1, 10000) for _ in range(4)])
                 for _ in range(30000)]))
    # duplicates-heavy
    cases = []
    for _ in range(5000):
        v = rnd.randint(1, 10000)
        a = [v, v, rnd.randint(1, 10000), rnd.randint(1, 10000)]
        rnd.shuffle(a)
        cases.append(case(a))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
