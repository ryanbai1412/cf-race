import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def rand_case(rnd, nmax):
    n = rnd.randint(1, nmax)
    vmax = rnd.choice([n, max(1, n // 2), max(1, min(n, 3))])
    return case([rnd.randint(1, vmax) for _ in range(n)])


def main(outdir):
    rnd = random.Random(1714)
    w = Writer(outdir)
    # edge: n=1, all equal, all distinct, duplicate at both ends
    w.add(multi([case([1]), case([1, 1, 1, 1]), case([1, 2, 3, 4]),
                 case([1, 2, 3, 1]), case([2, 2]), case([1, 2, 2, 3])]))
    # random small
    for _ in range(3):
        w.add(multi([rand_case(rnd, 8) for _ in range(200)]))
    # random medium
    for _ in range(3):
        w.add(multi([rand_case(rnd, 200) for _ in range(100)]))
    # max size: sum n = 2e5 in one big case + many tiny cases
    w.add(case([rnd.randint(1, 200000) for _ in range(200000)]).replace(
        "200000\n", "1\n200000\n", 1))
    w.add(multi([case([rnd.randint(1, 100) for _ in range(rnd.randint(1, 30))])
                 for _ in range(10000)]))
    # all-equal max
    w.add(multi([case([7] * 100000)]))


if __name__ == "__main__":
    main(sys.argv[1])
