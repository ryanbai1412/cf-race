import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(r, b):
    return f"{len(r)}\n{r}\n{b}"


def rand_case(rnd, n):
    r = "".join(str(rnd.randint(0, 9)) for _ in range(n))
    b = "".join(str(rnd.randint(0, 9)) for _ in range(n))
    return case(r, b)


def main(outdir):
    rnd = random.Random(1459)
    w = Writer(outdir)
    # edge: n=1 all combos of relations
    w.add(multi([case("5", "3"), case("3", "5"), case("7", "7"),
                 case("0", "0"), case("0", "9"), case("9", "0")]))
    # equal strings -> EQUAL
    w.add(multi([case("123", "123"), case("0" * 10, "0" * 10)]))
    # random small, full t
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(1, 20)) for _ in range(100)]))
    # correlated digits (many ties)
    cases = []
    for _ in range(100):
        n = rnd.randint(1, 50)
        r = [rnd.randint(0, 9) for _ in range(n)]
        b = [min(9, max(0, x + rnd.choice([-1, 0, 0, 0, 1]))) for x in r]
        cases.append(case("".join(map(str, r)), "".join(map(str, b))))
    w.add(multi(cases))
    # max size: 100 cases of n=1000
    w.add(multi([rand_case(rnd, 1000) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
