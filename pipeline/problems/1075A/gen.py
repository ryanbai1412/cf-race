import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


N = 10 ** 18


def case(n, x, y):
    return f"{n}\n{x} {y}"


def main(outdir):
    rnd = random.Random(1075)
    w = Writer(outdir)
    w.add(case(2, 1, 1))
    w.add(case(2, 1, 2))
    w.add(case(2, 2, 1))
    w.add(case(2, 2, 2))
    w.add(case(N, 1, 1))
    w.add(case(N, N, N))
    w.add(case(N, N // 2, N // 2))            # exact middle-ish, white wins
    w.add(case(N, N // 2 + 1, N // 2 + 1))    # just past middle
    w.add(case(N, 1, N))
    w.add(case(N, N, 1))
    w.add(case(3, 2, 2))
    w.add(case(5, 3, 3))
    w.add(case(5, 3, 4))
    for _ in range(4):
        n = rnd.randint(2, 20)
        w.add(case(n, rnd.randint(1, n), rnd.randint(1, n)))
    for _ in range(4):
        n = rnd.randint(2, N)
        w.add(case(n, rnd.randint(1, n), rnd.randint(1, n)))


if __name__ == "__main__":
    main(sys.argv[1])
