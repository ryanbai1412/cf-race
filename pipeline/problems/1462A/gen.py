import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(b):
    return f"{len(b)}\n{' '.join(map(str, b))}"


def main(outdir):
    rnd = random.Random(1462)
    w = Writer(outdir)
    # edge: n=1, n=2
    w.add(multi([case([1]), case([1000000000]), case([5, 7])]))
    # small n, all sizes 1..10
    w.add(multi([case([rnd.randint(1, 100) for _ in range(n)])
                 for n in range(1, 11)]))
    # random, full t=300
    for _ in range(2):
        w.add(multi([case([rnd.randint(1, 10 ** 9)
                           for _ in range(rnd.randint(1, 50))])
                     for _ in range(300)]))
    # max: 300 cases of n=300
    w.add(multi([case([rnd.randint(1, 10 ** 9) for _ in range(300)])
                 for _ in range(300)]))
    # distinct values so answer order is fully checkable
    w.add(multi([case(rnd.sample(range(1, 10 ** 9), 299))]))


if __name__ == "__main__":
    main(sys.argv[1])
