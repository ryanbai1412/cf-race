import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(m, a):
    return f"{len(a)} {m}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(16971)
    w = Writer(outdir)
    # edge cases
    edge = [
        case(1, [1]),
        case(10**4, [1]),
        case(1, [100]),
        case(10**4, [100] * 100),
        case(1, [100] * 100),
        case(100, [100]),
        case(99, [100]),
        case(101, [100]),
    ]
    w.add(multi(edge))
    # small randoms
    for _ in range(4):
        cases = [case(rnd.randint(1, 30),
                      [rnd.randint(1, 10) for _ in range(rnd.randint(1, 10))])
                 for _ in range(100)]
        w.add(multi(cases))
    # m near sum(a) (answer near 0 boundary)
    cases = []
    for _ in range(100):
        n = rnd.randint(1, 100)
        a = [rnd.randint(1, 100) for _ in range(n)]
        s = sum(a)
        m = max(1, min(10**4, s + rnd.randint(-3, 3)))
        cases.append(case(m, a))
    w.add(multi(cases))
    # max-size: t = 100, n = 100
    cases = [case(rnd.randint(1, 10**4),
                  [rnd.randint(1, 100) for _ in range(100)])
             for _ in range(100)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
