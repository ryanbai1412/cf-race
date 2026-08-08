import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b):
    return f"{a} {b}"


def main(outdir):
    rnd = random.Random(1482)
    w = Writer(outdir)

    # edge cases: smallest, largest, degenerate rows/columns
    w.add(multi([case(1, 1), case(1, 2), case(2, 1), case(1, 100), case(100, 1),
                 case(100, 100), case(2, 2), case(99, 100), case(100, 99), case(50, 50)]))

    # all small pairs
    cases = [case(a, b) for a in range(1, 11) for b in range(1, 11)]
    w.add(multi(cases[:100]))

    # random tests
    for _ in range(6):
        cases = [case(rnd.randint(1, 100), rnd.randint(1, 100))
                 for _ in range(rnd.randint(1, 100))]
        w.add(multi(cases))

    # max t with max values
    w.add(multi([case(100, 100) for _ in range(100)]))
    # squares and thin strips
    w.add(multi([case(k, k) for k in range(1, 51)] + [case(1, k) for k in range(1, 51)]))


if __name__ == "__main__":
    main(sys.argv[1])
