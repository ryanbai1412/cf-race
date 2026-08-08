import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b, c, d):
    return f"{a} {b} {c} {d}"


def rand_case(rnd, hi=10**4):
    vals = rnd.sample(range(0, hi + 1), 4)
    return case(*vals)


def main(outdir):
    rnd = random.Random(16921)
    w = Writer(outdir)
    # edge cases: Timur first / last / middle, extremes
    edge = [
        case(10000, 0, 1, 2),
        case(0, 1, 2, 3),
        case(2, 0, 1, 3),
        case(9999, 10000, 9998, 9997),
        case(0, 10000, 9999, 9998),
        case(1, 0, 2, 3),
    ]
    w.add(multi(edge))
    # small-range randoms (lots of near-ties)
    for _ in range(4):
        cases = [case(*rnd.sample(range(0, 8), 4)) for _ in range(200)]
        w.add(multi(cases))
    # full-range randoms
    for _ in range(4):
        cases = [rand_case(rnd) for _ in range(500)]
        w.add(multi(cases))
    # max-size: t = 10^4
    cases = [rand_case(rnd) for _ in range(10**4)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
