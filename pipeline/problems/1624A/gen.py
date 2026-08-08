import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MX = 10**9


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1624)
    w = Writer(outdir)

    # edges: n=1, all equal, extremes
    w.add(
        multi(
            [
                case([1]),
                case([MX]),
                case([1, MX]),
                case([MX, 1]),
                case([7] * 50),
                case([1] * 49 + [MX]),
                case([MX] * 49 + [1]),
                case(list(range(1, 51))),
            ]
        )
    )

    # small values
    for _ in range(2):
        w.add(
            multi(
                [
                    case([rnd.randint(1, 5) for _ in range(rnd.randint(1, 8))])
                    for _ in range(5000)
                ]
            )
        )
    # general random
    w.add(
        multi(
            [
                case([rnd.randint(1, MX) for _ in range(rnd.randint(1, 50))])
                for _ in range(3000)
            ]
        )
    )
    # max t, tiny n
    w.add(multi([case([rnd.randint(1, MX)]) for _ in range(10**4)]))
    # max n every case
    w.add(multi([case([rnd.randint(1, MX) for _ in range(50)]) for _ in range(2000)]))


if __name__ == "__main__":
    main(sys.argv[1])
