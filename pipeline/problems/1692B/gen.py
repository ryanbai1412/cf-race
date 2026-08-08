import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def rand_case(rnd, n, hi):
    return case([rnd.randint(1, hi) for _ in range(n)])


def main(outdir):
    rnd = random.Random(16922)
    w = Writer(outdir)
    # edge cases
    edge = [
        case([1]),
        case([7, 7]),
        case([1, 2]),
        case([5] * 50),
        case([5] * 49),
        case(list(range(1, 51))),
        case([1, 1, 2, 2, 3, 3]),
        case([1, 1, 1, 2]),
        case([10000, 10000, 1]),
    ]
    w.add(multi(edge))
    # small random with heavy duplicates
    for hi in (1, 2, 3, 5):
        cases = [rand_case(rnd, rnd.randint(1, 12), hi) for _ in range(120)]
        w.add(multi(cases))
    # full-range randoms
    for _ in range(3):
        cases = [rand_case(rnd, rnd.randint(1, 50), rnd.choice([10, 100, 10**4]))
                 for _ in range(100)]
        w.add(multi(cases))
    # max-size: t = 1000, n = 50 each
    cases = [rand_case(rnd, 50, rnd.choice([3, 25, 10**4])) for _ in range(1000)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
