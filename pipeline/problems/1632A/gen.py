import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def rand_str(rnd, n):
    return "".join(rnd.choice("01") for _ in range(n))


def main(outdir):
    rnd = random.Random(1632)
    w = Writer(outdir)
    # all strings of length 1 and 2, plus small length-3 samples
    small = ["0", "1", "00", "01", "10", "11", "000", "010", "101", "111"]
    w.add(multi([case(s) for s in small]))
    # max length edge cases
    w.add(multi([case("0" * 100), case("1" * 100), case("01" * 50), case("10" * 50)]))
    # random tests, biased toward tiny n
    for seed in range(8):
        cases = []
        for _ in range(100):
            n = rnd.choice([1, 1, 2, 2, 2, 3, rnd.randint(1, 100)])
            cases.append(case(rand_str(rnd, n)))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
