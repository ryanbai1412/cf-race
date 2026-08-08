import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10**7


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(16762)
    w = Writer(outdir)
    # edges: n=1, all equal, max values, min mixed with max
    edge = [
        case([1]),
        case([M]),
        case([M] * 50),
        case([1] * 50),
        case([1] + [M] * 49),
        case([M] * 49 + [1]),
        case([1, M]),
    ]
    w.add(multi(edge))
    # random small
    for _ in range(4):
        cs = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randint(1, 10)
            cs.append(case([rnd.randint(1, 20) for _ in range(n)]))
        w.add(multi(cs))
    # random large values
    for _ in range(4):
        cs = []
        for _ in range(rnd.randint(1, 200)):
            n = rnd.randint(1, 50)
            cs.append(case([rnd.randint(1, M) for _ in range(n)]))
        w.add(multi(cs))
    # max: t=1000, n=50, max values
    cs = [case([rnd.randint(1, M) for _ in range(50)]) for _ in range(1000)]
    w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
