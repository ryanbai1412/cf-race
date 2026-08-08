import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = (1 << 30) - 1


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1635)
    w = Writer(outdir)
    # edges: zeros, max values, n=2
    w.add(multi([case([0, 0]), case([0, MAXV]), case([MAXV, MAXV]),
                 case([MAXV] * 100), case([0] * 100), case([1, 2])]))
    # random tests with varied value ranges
    for seed in range(8):
        cases = []
        for _ in range(125):
            n = rnd.randint(2, 100)
            hi = rnd.choice([1, 3, 15, 255, MAXV])
            cases.append(case([rnd.randint(0, hi) for _ in range(n)]))
        w.add(multi(cases))
    # max test: t=1000 cases of n=100 max-range values
    cases = [case([rnd.randint(0, MAXV) for _ in range(100)]) for _ in range(1000)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
