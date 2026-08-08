import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_case(rnd, n):
    return "".join(rnd.choice("EN") for _ in range(n))


def main(outdir):
    rnd = random.Random(1620)
    w = Writer(outdir)
    # exhaustive n=2..4
    small = []
    for n in range(2, 5):
        for mask in range(2 ** n):
            small.append("".join("EN"[(mask >> i) & 1] for i in range(n)))
    w.add(multi(small[:28]))
    # edges: all E, all N, exactly one N at various positions
    w.add(multi([
        "E" * 50, "N" * 50, "N" * 49 + "E",
        "N" + "E" * 49, "E" * 49 + "N", "E" * 25 + "N" + "E" * 24,
        "NN" + "E" * 48, "EN", "NE", "NN", "EE",
    ]))
    # random with heavy E bias (more single-N cases)
    for _ in range(4):
        cases = []
        for _ in range(250):
            n = rnd.randint(2, 50)
            s = "".join("N" if rnd.random() < 0.06 else "E"
                        for _ in range(n))
            cases.append(s)
        w.add(multi(cases))
    # uniform random, max t
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(2, 50))
                     for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
