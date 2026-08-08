import itertools
import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1760)
    w = Writer(outdir)
    # all triples of distinct values 1..20 in all orders = 6840 = max t
    allc = [f"{a} {b} {c}" for a, b, c in itertools.permutations(range(1, 21), 3)]
    w.add(multi(allc))
    # edges
    w.add(multi(["1 2 3", "3 2 1", "2 3 1", "1 19 20", "20 1 19", "19 20 1"]))
    # random
    for _ in range(4):
        cases = []
        for _ in range(rnd.randint(1, 1000)):
            a, b, c = rnd.sample(range(1, 21), 3)
            cases.append(f"{a} {b} {c}")
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
