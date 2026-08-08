import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(arr):
    return f"{len(arr)}\n" + " ".join(map(str, arr))


def main(outdir):
    rnd = random.Random(1300)
    w = Writer(outdir)
    w.add(multi([case([0]), case([-1]), case([1]), case([100]),
                 case([-100])]))
    w.add(multi([case([0] * 100)]))
    w.add(multi([case([-1] * 100)]))
    w.add(multi([case([-1, 1] * 50)]))
    # sum becomes zero after fixing zeros
    w.add(multi([case([-1, 0]), case([-2, 0, 1]), case([0, 0, -2])]))
    # max: t=1000
    for _ in range(4):
        w.add(multi([case([rnd.randint(-100, 100)
                           for _ in range(rnd.randint(1, 100))])
                     for _ in range(1000)]))
    # zero-heavy
    for _ in range(4):
        cases = []
        for _ in range(200):
            n = rnd.randint(1, 20)
            cases.append(case([rnd.choice([0, 0, -1, 1, rnd.randint(-5, 5)])
                               for _ in range(n)]))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
