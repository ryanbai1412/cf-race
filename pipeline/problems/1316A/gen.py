import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, m, a):
    return f"{n} {m}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1316)
    w = Writer(outdir)
    # edges
    w.add(multi([case(1, 1, [0]), case(1, 100000, [100000]),
                 case(2, 100000, [100000, 100000]),
                 case(1000, 1, [0] * 1000), case(1000, 1, [1] * 1000)]))
    w.add(multi([case(1000, 100000, [100000] * 1000),
                 case(1000, 100000, [0] * 1000)]))
    # small random
    for _ in range(5):
        cases = []
        for _ in range(200):
            n = rnd.randint(1, 8)
            m = rnd.randint(1, 15)
            cases.append(case(n, m, [rnd.randint(0, m) for _ in range(n)]))
        w.add(multi(cases))
    # max-size random (respect sum n <= large but keep input < 1MB)
    for _ in range(5):
        cases = []
        for _ in range(200):
            n = rnd.randint(1, 200)
            m = rnd.randint(1, 100000)
            cases.append(case(n, m, [rnd.randint(0, m) for _ in range(n)]))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
