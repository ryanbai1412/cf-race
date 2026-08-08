import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1678)
    w = Writer(outdir)
    # edges: all zeros, no zeros all distinct, duplicates without zeros, single zero
    edge = [
        case([0, 0]),
        case([0] * 100),
        case([1, 2]),
        case([5, 5]),
        case(list(range(1, 101))),
        case([100] * 100),
        case([0] + list(range(1, 100))),
        case([100, 99]),
    ]
    w.add(multi(edge))
    # random small values (zeros and duplicates common)
    for _ in range(5):
        cs = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randint(2, 10)
            cs.append(case([rnd.randint(0, 3) for _ in range(n)]))
        w.add(multi(cs))
    # random full range
    for _ in range(4):
        cs = []
        for _ in range(rnd.randint(1, 200)):
            n = rnd.randint(2, 100)
            cs.append(case([rnd.randint(0, 100) for _ in range(n)]))
        w.add(multi(cs))
    # distinct-only arrays (n+1 branch)
    cs = []
    for _ in range(100):
        n = rnd.randint(2, 100)
        vals = rnd.sample(range(1, 101), n)
        cs.append(case(vals))
    w.add(multi(cs))
    # max: t=1000, n=100
    cs = [case([rnd.randint(0, 100) for _ in range(100)]) for _ in range(1000)]
    w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
