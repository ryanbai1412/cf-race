import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXLEN = 10 ** 5
MAXT = 10 ** 4


def rand_string(rnd, n, p0):
    return "".join("0" if rnd.random() < p0 else "1" for _ in range(n))


def main(outdir):
    rnd = random.Random(1566)
    w = Writer(outdir)

    # edges: tiny strings covering all answers
    w.add(multi(["0", "1", "01", "10", "00", "11", "010", "101", "0110", "1001"]))
    # single zero block variants / multi block variants
    w.add(multi(["1" * 50 + "0" * 50, "0" * 100, "1" * 100,
                 "01" * 50, "10" * 50, "0" + "1" * 98 + "0"]))
    # max-size single strings
    w.add(multi(["0" * MAXLEN]))
    w.add(multi(["1" * MAXLEN]))
    w.add(multi([rand_string(rnd, MAXLEN, 0.5)]))
    w.add(multi(["1" * (MAXLEN // 2) + "0" * (MAXLEN - MAXLEN // 2)]))
    # max t: many tiny strings
    w.add(multi([rand_string(rnd, rnd.randint(1, 10), rnd.choice([0.1, 0.5, 0.9]))
                 for _ in range(MAXT)]))
    # random mixes with varying density, total length near the cap
    for p0 in (0.02, 0.3, 0.7, 0.98):
        cases, total = [], 0
        while total + 200 <= MAXLEN:
            n = rnd.randint(1, 200)
            cases.append(rand_string(rnd, n, p0))
            total += n
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
