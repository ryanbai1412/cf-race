import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(xs):
    return f"{len(xs)}\n{' '.join(map(str, xs))}"


def rand_case(rnd, n, hi=None):
    hi = hi or 2 * n
    return case(sorted(rnd.randint(1, hi) for _ in range(n)))


def main(outdir):
    rnd = random.Random(14666)
    w = Writer(outdir)
    # edge: n=1, all equal
    w.add(multi([case([1]), case([2]), case([1, 1]), case([1, 1, 1]),
                 case([5] * 10)]))
    # consecutive runs
    w.add(multi([case(list(range(1, 11))), case([1, 1, 2, 2, 3, 3]),
                 case([1, 2, 2, 3, 4, 4, 5])]))
    # random small, many cases
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(1, 8), rnd.randint(1, 16))
                     for _ in range(300)]))
    # dense (values from small range -> lots of dups)
    w.add(multi([rand_case(rnd, 50, 10) for _ in range(100)]))
    # max: n=1e5 single case
    w.add(multi([rand_case(rnd, 100000)]))
    # max t: 10000 tiny cases
    w.add(multi([rand_case(rnd, rnd.randint(1, 10)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
