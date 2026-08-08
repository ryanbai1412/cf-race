import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def main(outdir):
    rnd = random.Random(954)
    w = Writer(outdir)
    # edges
    w.add(case("U"))
    w.add(case("R"))
    w.add(case("U" * 100))
    w.add(case("R" * 100))
    w.add(case("UR" * 50))
    w.add(case("RU" * 50))
    # random tests
    for _ in range(10):
        n = rnd.randint(1, 100)
        w.add(case("".join(rnd.choice("UR") for _ in range(n))))
    # biased runs
    for p in (0.1, 0.9):
        n = rnd.randint(50, 100)
        w.add(case("".join("U" if rnd.random() < p else "R" for _ in range(n))))


if __name__ == "__main__":
    main(sys.argv[1])
