import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, x, h):
    return f"{n} {x}\n" + " ".join(map(str, h))


def rand_case(rnd, nmax=100):
    n = rnd.randint(1, nmax)
    x = rnd.randint(1, 1000)
    h = [rnd.randint(1, 1000) for _ in range(2 * n)]
    return case(n, x, h)


def yes_case(rnd, nmax=100):
    n = rnd.randint(1, nmax)
    x = rnd.randint(1, 500)
    front = [rnd.randint(1, 500) for _ in range(n)]
    back = [f + x + rnd.randint(0, 500) for f in front]
    h = front + back
    rnd.shuffle(h)
    return case(n, x, h)


def main(outdir):
    rnd = random.Random(1705)
    w = Writer(outdir)
    # edge: n=1
    w.add(multi([case(1, 1, [1, 2]), case(1, 1000, [1, 1000]),
                 case(1, 1000, [1000, 1000]), case(1, 1, [1000, 1000])]))
    # all-equal heights, tight boundary diffs
    w.add(multi([case(3, 5, [10, 10, 10, 15, 15, 15]),
                 case(3, 5, [10, 10, 10, 15, 15, 14]),
                 case(2, 1000, [1, 1, 1000, 1000])]))
    # random small
    for seed in range(3):
        w.add(multi([rand_case(rnd, 10) for _ in range(100)]))
    # random mixed yes/no
    for seed in range(3):
        cs = [yes_case(rnd, 50) if rnd.random() < 0.5 else rand_case(rnd, 50)
              for _ in range(100)]
        w.add(multi(cs))
    # max size: t=100, n=100
    w.add(multi([rand_case(rnd, 100) for _ in range(100)]))
    w.add(multi([yes_case(rnd, 100) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
