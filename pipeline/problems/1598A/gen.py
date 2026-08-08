import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(r1, r2):
    return f"{len(r1)}\n{r1}\n{r2}"


def rand_case(rnd, n, p):
    while True:
        r1 = ["1" if rnd.random() < p else "0" for _ in range(n)]
        r2 = ["1" if rnd.random() < p else "0" for _ in range(n)]
        r1[0] = "0"
        r2[-1] = "0"
        return case("".join(r1), "".join(r2))


def main(outdir):
    rnd = random.Random(1598)
    w = Writer(outdir)
    # edge: all safe, fully blocked column, blocked at ends
    w.add(multi([
        case("000", "000"),
        case("010", "010"),
        case("011", "110"),
        case("001", "100"),
        case("0" + "1" * 99, "1" * 99 + "0"),
        case("0" * 100, "0" * 100),
    ]))
    # random small with varied trap density
    for p in (0.2, 0.35, 0.5):
        w.add(multi([rand_case(rnd, rnd.randint(3, 10), p) for _ in range(100)]))
    # random large
    for p in (0.1, 0.3, 0.5, 0.7):
        w.add(multi([rand_case(rnd, rnd.randint(50, 100), p) for _ in range(100)]))
    # max-size: t = 100, n = 100
    w.add(multi([rand_case(rnd, 100, 0.4) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
