import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def rand_case(rnd, n):
    return case([rnd.randint(1, 2) for _ in range(n)])


def main(outdir):
    rnd = random.Random(1472)
    w = Writer(outdir)
    # edges: n=1, n=2 combos
    w.add(multi([case([1]), case([2]), case([1, 1]), case([2, 2]),
                 case([1, 2]), case([1, 1, 1]), case([2, 2, 2]),
                 case([1, 1, 2]), case([1, 2, 2])]))
    # parity-focused: odd twos with 0/1/2 ones
    w.add(multi([case([2] * 5), case([2] * 5 + [1]), case([2] * 5 + [1, 1]),
                 case([2] * 4 + [1, 1]), case([1] * 99), case([1] * 100)]))
    # random small, many cases
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(1, 10)) for _ in range(500)]))
    # max: t=1e4 with sum n = 1e5 (n<=100 each)
    cases = []
    tot = 0
    for _ in range(10000):
        n = rnd.randint(1, 10)
        tot += n
        cases.append(rand_case(rnd, n))
    w.add(multi(cases))
    # all n=100 cases
    w.add(multi([rand_case(rnd, 100) for _ in range(300)]))


if __name__ == "__main__":
    main(sys.argv[1])
