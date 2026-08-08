import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b, c, d, e, f):
    return "\n".join(map(str, [a, b, c, d, e, f]))


def main(outdir):
    rnd = random.Random(1271)
    w = Writer(outdir)
    M = 100000
    w.add(case(1, 1, 1, 1, 1, 1))
    w.add(case(M, M, M, M, 1000, 1000))
    w.add(case(M, 1, 1, M, 1000, 1))
    w.add(case(1, M, M, M, 1, 1000))
    w.add(case(M, M, M, 1, 500, 999))
    # tie: e vs f equal
    w.add(case(10, 10, 10, 5, 7, 7))
    for _ in range(10):
        w.add(case(*(rnd.randint(1, M) for _ in range(4)),
                   rnd.randint(1, 1000), rnd.randint(1, 1000)))
    for _ in range(4):
        w.add(case(*(rnd.randint(1, 5) for _ in range(4)),
                   rnd.randint(1, 10), rnd.randint(1, 10)))


if __name__ == "__main__":
    main(sys.argv[1])
