import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_case(rnd):
    l1 = rnd.randint(1, 50)
    r1 = rnd.randint(l1, 50)
    l2 = rnd.randint(1, 50)
    r2 = rnd.randint(l2, 50)
    return f"{l1} {r1} {l2} {r2}"


def main(outdir):
    rnd = random.Random(16801)
    w = Writer(outdir)
    # all interval relationships: overlap, touch, disjoint, nested, equal, extremes
    edge = [
        "1 1 1 1",
        "50 50 50 50",
        "1 50 1 50",
        "1 1 50 50",
        "50 50 1 1",
        "1 25 25 50",
        "1 24 25 50",
        "26 50 1 25",
        "10 20 12 18",
        "5 5 5 5",
        "1 50 25 25",
    ]
    w.add(multi(edge))
    # exhaustive over point intervals l1=r1, l2=r2 (2500 cases)
    cs = [f"{i} {i} {j} {j}" for i in range(1, 51) for j in range(1, 51)]
    w.add(multi(cs))
    # random
    for _ in range(5):
        w.add(multi([rand_case(rnd) for _ in range(rnd.randint(1, 500))]))
    # max t
    w.add(multi([rand_case(rnd) for _ in range(5000)]))


if __name__ == "__main__":
    main(sys.argv[1])
