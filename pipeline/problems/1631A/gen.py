import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MX = 10000


def case(a, b):
    n = len(a)
    return f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}"


def rand_case(rnd, nmax, vmax):
    n = rnd.randint(1, nmax)
    return case(
        [rnd.randint(1, vmax) for _ in range(n)],
        [rnd.randint(1, vmax) for _ in range(n)],
    )


def main(outdir):
    rnd = random.Random(1631)
    w = Writer(outdir)

    # edges: n=1, all equal, extremes on one side
    w.add(
        multi(
            [
                case([1], [1]),
                case([MX], [1]),
                case([MX], [MX]),
                case([1] * 100, [MX] * 100),
                case([MX] * 100, [MX] * 100),
                case([1] * 99 + [MX], [MX] + [1] * 99),
                case(list(range(1, 101)), list(range(100, 0, -1))),
            ]
        )
    )

    # tiny values / tiny n (stress region)
    for _ in range(2):
        w.add(multi([rand_case(rnd, 5, 5) for _ in range(100)]))
    # general
    w.add(multi([rand_case(rnd, 100, MX) for _ in range(100)]))
    # max t and max n
    w.add(multi([rand_case(rnd, 100, MX) for _ in range(100)]))
    w.add(multi([case([rnd.randint(1, MX) for _ in range(100)], [rnd.randint(1, MX) for _ in range(100)]) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
