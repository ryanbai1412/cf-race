import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10 ** 9


def case(n, B, x, y):
    return f"{n} {B} {x} {y}"


def main(outdir):
    rnd = random.Random(16572)
    w = Writer(outdir)
    # edge cases
    w.add(multi([
        case(1, 1, 1, 1), case(1, MAX, MAX, MAX), case(1, 1, MAX, MAX),
        case(2, 1, 2, 1), case(5, 100, 1, MAX), case(5, 1, 2, MAX),
        case(10, MAX, MAX, 1), case(3, 1, 1, 1),
    ]))
    # x always fits / x never fits after first step
    w.add(multi([case(20, MAX, 1, 1), case(20, 1, 1, 1),
                 case(20, 5, 3, 2), case(20, 5, 3, 7)]))
    # small random
    for _ in range(4):
        w.add(multi([case(rnd.randint(1, 20), rnd.randint(1, 30),
                          rnd.randint(1, 30), rnd.randint(1, 30))
                     for _ in range(1000)]))
    # large random values
    for _ in range(3):
        w.add(multi([case(rnd.randint(1, 200),
                          rnd.randint(1, MAX), rnd.randint(1, MAX),
                          rnd.randint(1, MAX)) for _ in range(1000)]))
    # max n in a single case
    w.add(multi([case(200000, rnd.randint(1, MAX),
                      rnd.randint(1, MAX), rnd.randint(1, MAX))]))
    w.add(multi([case(200000, 10, 3, 4)]))
    # max t with sum n = 2e5
    w.add(multi([case(20, rnd.randint(1, MAX), rnd.randint(1, MAX),
                      rnd.randint(1, MAX)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
