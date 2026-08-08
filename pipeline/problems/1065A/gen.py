import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


M = 10 ** 9


def case(s, a, b, c):
    return f"{s} {a} {b} {c}"


def main(outdir):
    rnd = random.Random(1065)
    w = Writer(outdir)
    w.add(multi([case(1, 1, 1, 1)]))
    w.add(multi([case(M, M, M, M)]))
    w.add(multi([case(M, 1, M, 1)]))          # maximal answer
    w.add(multi([case(1, 1, 1, M)]))          # can't buy anything
    w.add(multi([case(M - 1, 2, 3, 1)]))
    edge = [
        case(1, M, M, M), case(M, M, 1, 1), case(M, 1, 1, M),
        case(999999999, 999999937, 1000000000, 1),
        case(10, 3, 1, 1), case(10, 3, 1, 4), case(7, 7, 7, 1),
    ]
    w.add(multi(edge))
    # 100 random large cases, and small ones
    w.add(multi([case(*[rnd.randint(1, M) for _ in range(4)]) for _ in range(100)]))
    w.add(multi([case(*[rnd.randint(1, 20) for _ in range(4)]) for _ in range(100)]))
    w.add(multi([case(rnd.randint(1, M), rnd.randint(1, 3), rnd.randint(1, M),
                      rnd.randint(1, 3)) for _ in range(100)]))
    for _ in range(6):
        t = rnd.randint(1, 100)
        w.add(multi([case(*[rnd.choice([rnd.randint(1, 10), rnd.randint(1, M)])
                            for _ in range(4)]) for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
