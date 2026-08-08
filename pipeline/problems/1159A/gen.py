import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

N = 100


def case(s):
    return f"{len(s)}\n{s}\n"


def main(outdir):
    rnd = random.Random(1159)
    w = Writer(outdir)
    # single ops
    w.add(case("-"))
    w.add(case("+"))
    # all one kind at max length
    w.add(case("-" * N))
    w.add(case("+" * N))
    # balanced patterns
    w.add(case("-+" * (N // 2)))
    w.add(case("+-" * (N // 2)))
    w.add(case("-" * (N // 2) + "+" * (N // 2)))
    w.add(case("+" * (N // 2) + "-" * (N // 2)))
    # dips below zero in the middle
    w.add(case("++---+"))
    w.add(case("-----+++++"))
    # random
    for _ in range(6):
        n = rnd.randint(1, N)
        w.add(case("".join(rnd.choice("+-") for _ in range(n))))


if __name__ == "__main__":
    main(sys.argv[1])
