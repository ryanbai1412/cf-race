import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXTOT = 200000


def rand_str(rnd, n, p=None):
    if p is None:
        p = rnd.random()
    return "".join("1" if rnd.random() < p else "0" for n_ in range(n))


def main(outdir):
    rnd = random.Random(1633)
    w = Writer(outdir)
    # tiny strings
    w.add(multi(["0", "1", "00", "01", "10", "11", "0011", "0101", "000111"]))
    # extremes: all same char, perfectly balanced max-size
    w.add(multi(["0" * MAXTOT]))
    w.add(multi(["1" * MAXTOT]))
    w.add(multi(["01" * (MAXTOT // 2)]))
    w.add(multi(["0" * (MAXTOT // 2) + "1" * (MAXTOT // 2)]))
    # many small random strings
    for seed in range(4):
        cases = []
        total = 0
        while total < MAXTOT - 60 and len(cases) < 10000:
            n = rnd.randint(1, 50)
            cases.append(rand_str(rnd, n))
            total += n
        w.add(multi(cases))
    # a few large random strings with varying density
    for p in (0.5, 0.5, 0.1, 0.9):
        n = rnd.randint(MAXTOT // 2, MAXTOT)
        w.add(multi([rand_str(rnd, n, p)]))


if __name__ == "__main__":
    main(sys.argv[1])
