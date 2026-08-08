import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, k, a):
    return f"{n} {k}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1516)
    w = Writer(outdir)
    # edges: minimal n, zeros, huge k
    w.add(multi([case(2, 1, [0, 0]), case(2, 10000, [100, 100]),
                 case(2, 1, [100, 0]), case(3, 1, [0, 100, 0])]))
    # k exhausted mid-array vs k larger than total sum
    w.add(multi([case(5, 3, [2, 2, 2, 2, 2]), case(5, 10000, [100] * 5),
                 case(4, 199, [100, 100, 0, 0])]))
    # max size: t=20, n=100, k=10000
    w.add(multi([case(100, 10000, [rnd.randint(0, 100) for _ in range(100)])
                 for _ in range(20)]))
    # all zeros / all max
    w.add(multi([case(100, 10000, [0] * 100), case(100, 10000, [100] * 100),
                 case(100, 1, [100] * 100)]))
    # random small
    for _ in range(6):
        cases = []
        for _ in range(rnd.randint(1, 20)):
            n = rnd.randint(2, 100)
            k = rnd.choice([1, rnd.randint(1, 50), rnd.randint(1, 10000)])
            cases.append(case(n, k, [rnd.randint(0, 100) for _ in range(n)]))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
