import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b, c):
    return f"{a} {b} {c}"


def main(outdir):
    rnd = random.Random(1236)
    w = Writer(outdir)
    # all-zero / all-max / single-axis extremes
    w.add(multi([case(0, 0, 0), case(100, 100, 100), case(0, 100, 100),
                 case(100, 0, 100), case(100, 100, 0), case(0, 0, 100),
                 case(100, 0, 0), case(0, 100, 0)]))
    # exhaustive small cube 0..4 split over a few tests (t <= 100)
    small = [case(a, b, c) for a in range(5) for b in range(5) for c in range(5)]
    for i in range(0, len(small), 100):
        w.add(multi(small[i:i + 100]))
    # cases where greedy order matters: plenty of c, scarce b
    w.add(multi([case(a, b, 100) for a in range(0, 101, 20) for b in range(0, 11)]))
    # b large, c tiny (op2 unusable)
    w.add(multi([case(a, 100, c) for a in range(0, 101, 25) for c in (0, 1)]))
    # odd/even parity boundaries on b and c
    w.add(multi([case(3, b, c) for b in range(0, 10) for c in range(0, 10)]))
    # random tests
    for _ in range(9):
        t = rnd.randint(1, 100)
        w.add(multi([case(rnd.randint(0, 100), rnd.randint(0, 100),
                          rnd.randint(0, 100)) for _ in range(t)]))
    # max-t all-max
    w.add(multi([case(100, 100, 100) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
