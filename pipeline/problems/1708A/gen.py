import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def yes_case(rnd, nmax=100):
    n = rnd.randint(2, nmax)
    a1 = rnd.randint(1, 31623)
    a = [a1] + [a1 * rnd.randint(1, 10 ** 9 // a1) for _ in range(n - 1)]
    return case(a)


def no_case(rnd, nmax=100):
    n = rnd.randint(2, nmax)
    a1 = rnd.randint(2, 31623)
    a = [a1] + [a1 * rnd.randint(1, 10 ** 9 // a1) for _ in range(n - 1)]
    i = rnd.randint(1, n - 1)
    a[i] = max(1, a[i] - rnd.randint(1, a1 - 1))
    return case(a)


def main(outdir):
    rnd = random.Random(1708)
    w = Writer(outdir)
    # edge: a1=1 (always YES), n=2, huge values
    w.add(multi([case([1, 10 ** 9]), case([10 ** 9, 10 ** 9]),
                 case([10 ** 9, 999999999]), case([2, 1]),
                 case([1] * 100)]))
    # tight divisibility boundaries
    w.add(multi([case([3, 999999999]), case([3, 1000000000]),
                 case([7, 7, 7, 14, 13]), case([5, 10, 15, 21])]))
    # random small values
    for _ in range(3):
        w.add(multi([case([rnd.randint(1, 20) for _ in range(rnd.randint(2, 8))])
                     for _ in range(100)]))
    # random mixed yes/no
    for _ in range(3):
        w.add(multi([yes_case(rnd, 50) if rnd.random() < 0.5 else no_case(rnd, 50)
                     for _ in range(100)]))
    # max size
    w.add(multi([yes_case(rnd) if rnd.random() < 0.5 else no_case(rnd)
                 for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
