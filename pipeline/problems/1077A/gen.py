import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


M = 10 ** 9


def case(a, b, k):
    return f"{a} {b} {k}"


def main(outdir):
    rnd = random.Random(1077)
    w = Writer(outdir)
    w.add(multi([case(1, 1, 1)]))
    w.add(multi([case(M, 1, M)]))             # maximum positive
    w.add(multi([case(1, M, M)]))             # maximum negative
    w.add(multi([case(M, M, M)]))             # cancels (k even? M is odd)
    w.add(multi([case(M, M, M - 1)]))
    edge = [
        case(1, 1, 2), case(1, 1, 3), case(M, M, 1), case(M, M, 2),
        case(M, 1, 1), case(1, M, 2), case(M, 1, M - 1), case(1, M, M - 1),
    ]
    w.add(multi(edge))
    w.add(multi([case(rnd.randint(1, M), rnd.randint(1, M), rnd.randint(1, M))
                 for _ in range(1000)]))
    w.add(multi([case(rnd.randint(1, 10), rnd.randint(1, 10), rnd.randint(1, 10))
                 for _ in range(1000)]))
    w.add(multi([case(M, M, rnd.randint(1, M)) for _ in range(1000)]))
    for _ in range(6):
        t = rnd.randint(1, 1000)
        w.add(multi([case(rnd.choice([rnd.randint(1, 5), rnd.randint(1, M)]),
                          rnd.choice([rnd.randint(1, 5), rnd.randint(1, M)]),
                          rnd.choice([rnd.randint(1, 5), rnd.randint(1, M)]))
                     for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
