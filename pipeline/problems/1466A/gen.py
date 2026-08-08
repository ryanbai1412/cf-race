import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(xs):
    return f"{len(xs)}\n{' '.join(map(str, xs))}"


def rand_case(rnd, n):
    return case(sorted(rnd.sample(range(1, 51), n)))


def main(outdir):
    rnd = random.Random(1466)
    w = Writer(outdir)
    # edge: n=1 (no triangle), n=2
    w.add(multi([case([1]), case([50]), case([1, 50]), case([1, 2])]))
    # max: all 50 points
    w.add(multi([case(list(range(1, 51)))]))
    # random, full t
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(1, 50)) for _ in range(100)]))
    # clustered / arithmetic patterns
    cases = [case(list(range(1, 50, 2))), case([1, 2, 4, 8, 16, 32]),
             case([x for x in range(1, 51) if x % 5 in (0, 1)])]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
