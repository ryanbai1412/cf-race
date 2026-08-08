import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, d, a):
    return f"{n} {d}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1307)
    w = Writer(outdir)
    # edge cases
    w.add(multi([case(1, 1, [0]), case(1, 100, [100]), case(2, 1, [0, 100])]))
    w.add(multi([case(100, 100, [0] * 99 + [100]),
                 case(100, 1, [100] * 100),
                 case(100, 100, [100] * 100)]))
    # random small
    for _ in range(6):
        cases = []
        for _ in range(100):
            n = rnd.randint(1, 10)
            d = rnd.randint(1, 20)
            cases.append(case(n, d, [rnd.randint(0, 10) for _ in range(n)]))
        w.add(multi(cases))
    # random max-size
    for _ in range(6):
        cases = []
        for _ in range(100):
            n = rnd.randint(1, 100)
            d = rnd.randint(1, 100)
            cases.append(case(n, d, [rnd.randint(0, 100) for _ in range(n)]))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
