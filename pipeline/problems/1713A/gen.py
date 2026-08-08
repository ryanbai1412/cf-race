import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(pts):
    return f"{len(pts)}\n" + "\n".join(f"{x} {y}" for x, y in pts)


def rand_pt(rnd, lim=100):
    if rnd.random() < 0.5:
        return (rnd.randint(-lim, lim), 0)
    return (0, rnd.randint(-lim, lim))


def rand_case(rnd, nmax=100, lim=100):
    return case([rand_pt(rnd, lim) for _ in range(rnd.randint(1, nmax))])


def main(outdir):
    rnd = random.Random(1713)
    w = Writer(outdir)
    # edge: single box at origin, extremes on each semi-axis
    w.add(multi([case([(0, 0)]), case([(100, 0)]), case([(-100, 0)]),
                 case([(0, 100)]), case([(0, -100)]),
                 case([(100, 0), (-100, 0), (0, 100), (0, -100)])]))
    # duplicates and one-sided
    w.add(multi([case([(5, 0)] * 100), case([(0, 0)] * 100),
                 case([(1, 0), (2, 0), (3, 0)]),
                 case([(0, -1), (0, -50)])]))
    # random small
    for _ in range(3):
        w.add(multi([rand_case(rnd, 5, 5) for _ in range(100)]))
    # random mixed
    for _ in range(3):
        w.add(multi([rand_case(rnd, 50) for _ in range(100)]))
    # max size
    w.add(multi([rand_case(rnd, 100) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
