import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def rand_s(rnd, n, p_one):
    return "".join("1" if rnd.random() < p_one else "0" for _ in range(n))


def main(outdir):
    rnd = random.Random(1658)
    w = Writer(outdir)
    # edge cases
    w.add(multi([case("0"), case("1"), case("00"), case("11"), case("01"),
                 case("010"), case("0110"), case("000")]))
    # all zeros / all ones at max length
    w.add(multi([case("0" * 100), case("1" * 100),
                 case("01" * 50), case("0110" * 25)]))
    # small exhaustive lengths 1..8
    strs = []
    for n in range(1, 9):
        for m in range(2 ** n):
            strs.append(case(format(m, f"0{n}b")))
    for i in range(0, len(strs), 1000):
        w.add(multi(strs[i:i + 1000]))
    # random with varying densities, max n
    for p in (0.1, 0.3, 0.5, 0.7, 0.9):
        w.add(multi([case(rand_s(rnd, rnd.randint(1, 100), p))
                     for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
