import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, m, k):
    return f"{n} {m} {k}"


def main(outdir):
    rnd = random.Random(15192)
    w = Writer(outdir)
    # edges
    w.add(multi([case(1, 1, 0), case(1, 1, 1), case(1, 1, 10000),
                 case(100, 100, 9999), case(100, 100, 10000),
                 case(100, 100, 9998), case(1, 100, 99), case(100, 1, 99)]))
    # boundary k = n*m-1 +- 1
    cases = []
    for _ in range(100):
        n, m = rnd.randint(1, 100), rnd.randint(1, 100)
        k = n * m - 1 + rnd.choice([-1, 0, 0, 1])
        if 0 <= k <= 10000:
            cases.append(case(n, m, k))
    w.add(multi(cases[:100]))
    # fully random max-size batches
    for seed in range(3):
        w.add(multi([case(rnd.randint(1, 100), rnd.randint(1, 100),
                          rnd.randint(0, 10000)) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
