import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, m, a):
    return f"{n} {m}\n" + " ".join(map(str, a))


def rand_case(rnd, nmax=50, mmax=50):
    n = rnd.randint(1, nmax)
    m = rnd.randint(1, mmax)
    a = [rnd.randint(1, m) for _ in range(n)]
    return case(n, m, a)


def main(outdir):
    rnd = random.Random(1706)
    w = Writer(outdir)
    # edge: m=1, n=1, repeated same a
    w.add(multi([case(1, 1, [1]), case(3, 1, [1, 1, 1]),
                 case(1, 50, [25]), case(1, 50, [26]),
                 case(4, 2, [1, 1, 2, 2])]))
    # all same position repeated; middle position (odd m)
    w.add(multi([case(50, 50, [1] * 50), case(50, 49, [25] * 50),
                 case(2, 3, [2, 2]), case(3, 3, [2, 2, 2])]))
    # random small
    for _ in range(3):
        w.add(multi([rand_case(rnd, 6, 6) for _ in range(200)]))
    # random mixed
    for _ in range(3):
        w.add(multi([rand_case(rnd) for _ in range(300)]))
    # max size: t=2000, n=m=50
    w.add(multi([case(50, 50, [rnd.randint(1, 50) for _ in range(50)])
                 for _ in range(2000)]))


if __name__ == "__main__":
    main(sys.argv[1])
