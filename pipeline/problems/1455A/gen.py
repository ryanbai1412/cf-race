import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_num(rnd, length):
    s = str(rnd.randint(1, 9))
    s += "".join(str(rnd.randint(0, 9)) for _ in range(length - 1))
    return s


def main(outdir):
    rnd = random.Random(1455)
    w = Writer(outdir)
    # edge: tiny values
    w.add(multi(["1", "9", "10", "11", "99", "100"]))
    # powers of 10 and neighbours
    cases = []
    for k in (1, 2, 5, 50, 99):
        p = 10 ** k
        cases.extend([str(p - 1), str(p), str(p + 1)])
    w.add(multi(cases))
    # max length (just under 10^100)
    w.add(multi(["9" * 100, "1" + "0" * 99, rand_num(rnd, 100)]))
    # random lengths, full t
    for _ in range(3):
        cases = [rand_num(rnd, rnd.randint(1, 100)) for _ in range(100)]
        w.add(multi(cases))
    # numbers with many trailing zeros
    cases = []
    for _ in range(50):
        L = rnd.randint(2, 100)
        z = rnd.randint(1, L - 1)
        cases.append(rand_num(rnd, L - z) + "0" * z)
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
