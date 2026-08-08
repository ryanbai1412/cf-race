import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXN = 10 ** 5


def main(outdir):
    rnd = random.Random(1581)
    w = Writer(outdir)

    # edges: smallest values
    w.add(multi(["1", "2", "3", "4", "5"]))
    # single max n
    w.add(multi([str(MAXN)]))
    w.add(multi([str(MAXN - 1)]))
    # max t: 10^5 cases of n=1
    w.add(multi(["1"] * MAXN))
    # random splits summing to the cap
    for _ in range(3):
        cases, total = [], 0
        while total < MAXN:
            n = min(rnd.randint(1, 2000), MAXN - total)
            cases.append(str(n))
            total += n
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
