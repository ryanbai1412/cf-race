import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10 ** 9


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(16602)
    w = Writer(outdir)
    # edge cases
    w.add(multi([
        case([1]), case([2]), case([MAX]),
        case([1, 1]), case([2, 1]), case([2, 2]), case([3, 1]),
        case([MAX, MAX]), case([MAX, MAX - 1]), case([MAX, MAX - 2]),
        case([MAX] + [1] * 5),
    ]))
    # ties and near-ties at the top
    w.add(multi([case([5, 5, 5]), case([7, 6, 6]), case([8, 6, 6]),
                 case([1] * 10), case([10, 9, 1, 1])]))
    # small random (stress the boundary max-second<=1)
    for _ in range(3):
        w.add(multi([case([rnd.randint(1, 6)
                           for _ in range(rnd.randint(1, 6))])
                     for _ in range(2000)]))
    # large values random
    for _ in range(2):
        w.add(multi([case([rnd.randint(MAX - 3, MAX)
                           for _ in range(rnd.randint(1, 10))])
                     for _ in range(1000)]))
    # max n single case (small values to keep file <1MB)
    w.add(multi([case([rnd.randint(1, 999) for _ in range(200000)])]))
    # large values, n capped so the file stays <1MB
    w.add(multi([case([MAX] * 80000)]))
    w.add(multi([case([rnd.randint(1, MAX) for _ in range(80000)])]))
    # max t, sum n = 2e5
    w.add(multi([case([rnd.randint(1, 3) for _ in range(20)])
                 for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
