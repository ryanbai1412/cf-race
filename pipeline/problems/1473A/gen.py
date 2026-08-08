import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, d, a):
    return f"{n} {d}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1473)
    w = Writer(outdir)

    # hand-made edge cases
    edge = [
        case(3, 1, [1, 1, 1]),                 # already ok, minimum n and d
        case(3, 1, [1, 1, 2]),                 # one bad, two smallest sum = 2 > d
        case(3, 100, [100, 100, 100]),         # max values, ok
        case(3, 2, [1, 1, 100]),               # replace with 1+1 = 2 = d
        case(3, 1, [100, 100, 100]),           # hopeless
        case(4, 4, [2, 2, 5, 5]),              # 2+2 = 4 = d
        case(4, 3, [2, 2, 5, 5]),              # 2+2 = 4 > d
        case(5, 3, [2, 3, 2, 5, 4]),
        case(3, 100, [1, 1, 1]),
        case(3, 99, [100, 1, 1]),              # max element just above d
    ]
    w.add(multi(edge))

    # small random tests (dense around the decision boundary)
    for _ in range(5):
        cases = []
        for _ in range(rnd.randint(1, 50)):
            n = rnd.randint(3, 6)
            d = rnd.randint(1, 12)
            cases.append(case(n, d, [rnd.randint(1, 12) for _ in range(n)]))
        w.add(multi(cases))

    # larger random tests over the full value range
    for _ in range(3):
        cases = []
        for _ in range(rnd.randint(100, 2000)):
            n = rnd.randint(3, 100)
            d = rnd.randint(1, 100)
            cases.append(case(n, d, [rnd.randint(1, 100) for _ in range(n)]))
        w.add(multi(cases))

    # max-size test: t = 2000, n = 100 everywhere
    cases = []
    for _ in range(2000):
        cases.append(case(100, rnd.randint(1, 100), [rnd.randint(1, 100) for _ in range(100)]))
    w.add(multi(cases))

    # all-equal arrays around every threshold
    cases = [case(3, d, [v, v, v]) for v in (1, 50, 100) for d in (1, 50, 99, 100)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
