import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXN = 10 ** 18
MAXQ = MAXN // 2050  # largest quotient allowed


def main(outdir):
    rnd = random.Random(1517)
    w = Writer(outdir)
    # edges
    w.add(multi(["1", "2049", "2050", "2051", "4100", str(MAXN),
                 str(2050 * MAXQ), str(2050 * MAXQ + 1),
                 str(2050 * 10 ** 14), str(2050 * (10 ** 14 - 1))]))
    # max digit-sum style quotients
    qs = [int("9" * d) for d in range(1, 15)] + [MAXQ, MAXQ - 1]
    w.add(multi([str(2050 * q) for q in qs]))
    # max size: T=1000 random mix
    for seed in range(4):
        cases = []
        for _ in range(1000):
            if rnd.random() < 0.6:
                cases.append(str(2050 * rnd.randint(1, MAXQ)))
            else:
                cases.append(str(rnd.randint(1, MAXN)))
        w.add(multi(cases))
    # small values around multiples
    w.add(multi([str(2050 * k + d) for k in range(1, 50)
                 for d in (-1, 0, 1)]))


if __name__ == "__main__":
    main(sys.argv[1])
